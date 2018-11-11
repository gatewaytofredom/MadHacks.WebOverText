package com.scrollingnumbers.wotclient;

import android.app.PendingIntent;
import android.content.Intent;
import android.net.VpnService;
import android.os.IBinder;
import android.os.ParcelFileDescriptor;
import android.util.Log;

import java.io.FileDescriptor;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.Executor;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class TextVpnService extends VpnService {

    //set constants such that all traffic is rerouted
    public static final String VPN_ADDRESS = "10.0.0.2";
    public static final String VPN_ROUTE = "0.0.0.0";
    public static final String SESSION_NAME = "WotClient";
    public static final String INTENT = "WotVPNIntent";
    public static final String TAG = TextVpnService.class.getSimpleName();

    private ParcelFileDescriptor vpnInterface;
    private ExecutorService executor;
    private ConcurrentLinkedQueue packetQueue;

    private PendingIntent pendingIntent;

    public TextVpnService() {
    }

    @Override
    public void onCreate() {
        super.onCreate();
        //setup VPN
        Builder builder = new Builder();
        builder.addAddress(VPN_ADDRESS, 32);
        builder.addRoute(VPN_ROUTE, 0);
        vpnInterface = builder.setSession("WOTClient").setConfigureIntent(pendingIntent).establish();

        packetQueue = new ConcurrentLinkedQueue<>();

        //set up threads for fetching packets onto queue and sending from the queue
        executor = Executors.newFixedThreadPool(2);
        //executor.submit();
        executor.submit(new VPNRunnable(vpnInterface.getFileDescriptor(), packetQueue));

        Log.i(TAG, "Threads started");
    }

    private static class VPNRunnable implements Runnable {

        private static final String TAG = VPNRunnable.class.getSimpleName();

        private FileDescriptor vpnDescriptor;
        private ConcurrentLinkedQueue queue;

        public VPNRunnable(FileDescriptor vpnDescriptor, ConcurrentLinkedQueue queue) {
            Log.i(TAG, "Initialized");
            this.vpnDescriptor = vpnDescriptor;
            this.queue = queue;
        }

        @Override
        public void run() {
            Log.i(TAG, "Started");

            FileChannel vpnInput = new FileInputStream(vpnDescriptor).getChannel();
            FileChannel vpnOutput = new FileOutputStream(vpnDescriptor).getChannel();

            boolean dataSent = true;
            boolean dataRecvd;

            try{
                ByteBuffer networkBuffer = null;
                while (!Thread.interrupted()) {
                    if (dataSent)
                        networkBuffer = ByteBufferPool.acquire();
                    else
                        networkBuffer.clear();

                    int readBytes = vpnInput.read(networkBuffer);
                    if (readBytes > 0) {
                        dataSent = true;
                        networkBuffer.flip();
                        Packet packet = new Packet(networkBuffer);
                        ByteBuffer backingBuffer = packet.backingBuffer;
                        int src, dest;
                        if (packet.isTCP()) {
                            src = packet.tcpHeader.sourcePort;
                            dest = packet.tcpHeader.destinationPort;
                        } else if (packet.isUDP()){
                            src = packet.udpHeader.sourcePort;
                            dest = packet.udpHeader.destinationPort;
                        } else {
                            src = 0;
                            dest = 0;
                        }
                        Log.i(TAG, String.format("Read bytes: %s", stringifyBuffer(backingBuffer)));
                        Log.i(TAG, String.format("Source: %s:%s",
                                packet.ip4Header.sourceAddress.toString(), Integer.toString(src)));
                        Log.i(TAG, String.format("Destination: %s:%s",
                                packet.ip4Header.destinationAddress.toString(), Integer.toString(dest)));
                    } else {
                        dataSent = false;
                    }

                    if (!dataSent) {
                        try {
                            Thread.sleep(10);
                        } catch (InterruptedException e) {
                        }
                    }
                }
            //} catch (InterruptedException e) {
                //Log.i(TAG, "Interrupted");
            } catch (IOException e) {
                Log.i(TAG, e.toString());
            } finally {
                try { vpnInput.close(); } catch (IOException e) {}
                try { vpnOutput.close(); } catch (IOException e) {}
            }
        }

        private String stringifyBuffer(ByteBuffer buf) {
            byte[] arr = new byte[buf.remaining()];
            buf.get(arr);
            String str = "[";
            for (byte b : arr) str += " " + Byte.toString(b);
            str += " ]";
            return str;
        }
    }


    /*@Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }*/
}
