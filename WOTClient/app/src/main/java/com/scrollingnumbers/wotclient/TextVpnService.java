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
import java.nio.channels.Selector;
import java.util.AbstractQueue;
import java.util.Queue;
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
    private ConcurrentLinkedQueue packetOutQueue;
    private ConcurrentLinkedQueue packetInQueue;
    private ConcurrentLinkedQueue textInQueue;
    private ConcurrentLinkedQueue textOutQueue;

    private Selector tcpSelector;

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

        packetOutQueue = new ConcurrentLinkedQueue<>();
        packetInQueue = new ConcurrentLinkedQueue<>();
        textInQueue = new ConcurrentLinkedQueue<>();
        textOutQueue = new ConcurrentLinkedQueue<>();

        try {
            tcpSelector = Selector.open();
        }
        catch (IOException e) {}

        //set up threads for fetching packets onto queue and sending from the queue
        executor = Executors.newFixedThreadPool(1);
        //executor.submit();
        executor.submit(new VPNRunnable(vpnInterface.getFileDescriptor(), packetOutQueue, packetInQueue));

        Log.i(TAG, "Threads started");
    }

    private static class VPNRunnable implements Runnable {

        private static final String TAG = VPNRunnable.class.getSimpleName();

        private FileDescriptor vpnDescriptor;
        private ConcurrentLinkedQueue outQueue;
        private ConcurrentLinkedQueue<ByteBuffer> inQueue;

        public VPNRunnable(FileDescriptor vpnDescriptor, ConcurrentLinkedQueue outQueue, ConcurrentLinkedQueue inQueue) {
            Log.i(TAG, "Initialized");
            this.vpnDescriptor = vpnDescriptor;
            this.outQueue = outQueue;
            this.inQueue = inQueue;
        }

        @Override
        public void run() {
            Log.i(TAG, "Started");

            FileChannel vpnInput = new FileInputStream(vpnDescriptor).getChannel();
            FileChannel vpnOutput = new FileOutputStream(vpnDescriptor).getChannel();


            boolean dataSent = true;
            boolean dataRecvd;

            try {
                ByteBuffer networkInBuffer = null;
                while (!Thread.interrupted()) {
                    Thread.sleep(10);
                    networkInBuffer = ByteBufferPool.acquire();

                    int readBytes = vpnInput.read(networkInBuffer);
                    if (readBytes > 0) {
                        networkInBuffer.flip();
                        Packet packet = new Packet(networkInBuffer);

                        if (packet.isTCP()) {
                            Log.i(TAG, "Recv'd TCP packet");
                            Log.i(TAG, String.format("FIN:%s, SYN:%s, RST:%s, PSH:%s, ACK:%s, URG:%s",
                                    packet.tcpHeader.isFIN(),
                                    packet.tcpHeader.isSYN(),
                                    packet.tcpHeader.isRST(),
                                    packet.tcpHeader.isPSH(),
                                    packet.tcpHeader.isACK(),
                                    packet.tcpHeader.isURG()));
                            if (packet.backingBuffer.remaining() == 0) {
                                if(packet.tcpHeader.isSYN()) {
                                    ByteBuffer response = ByteBufferPool.acquire();
                                    packet.updateTCPBuffer(response, (byte) (Packet.TCPHeader.SYN | Packet.TCPHeader.ACK)
                                        , packet.tcpHeader.sequenceNumber+1, packet.tcpHeader.acknowledgementNumber, 0);
                                    response.flip();
                                    vpnOutput.write(response);
                                    Log.i(TAG, "SYN-ACK Message Sent");
                                } else {
                                    Log.i(TAG, "Non-SYN header packet");
                                }
                            }
                            else {
                                Log.i(TAG, "Let there be a text");
                            }
                        } else if (packet.isUDP()){
                            Log.i(TAG, "Recvd UDP Packet");
                            ByteBuffer dnsResponse = ByteBufferPool.acquire();
                            dnsResponse.flip();
                            vpnOutput.write(dnsResponse);
                        } else { //unknown packet type --likely reached zeroes on ByteBufferPool
                            Log.i(TAG, "Unknown outgoing packet type.");
                        }
                    }
                }
            } catch (InterruptedException e) {
                Log.i(TAG, "Interrupted");
            } catch (IOException e) {
                Log.i(TAG, "" + e.getStackTrace()[0].getLineNumber());
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
