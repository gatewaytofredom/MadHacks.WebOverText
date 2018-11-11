package com.scrollingnumbers.wotclient;

import android.telephony.SmsManager;
import android.util.Log;

import java.util.concurrent.Callable;
import java.util.concurrent.ConcurrentLinkedQueue;

class SMSOut implements Runnable {
    public static final String TAG = SMSOut.class.getSimpleName();
    private ConcurrentLinkedQueue<String> textOutQueue;
    private SmsManager manager;

    public SMSOut(ConcurrentLinkedQueue textOutQueue) {
        this.textOutQueue = textOutQueue;
        this.manager = SmsManager.getDefault();
    }

    @Override
    public void run() {
        while (!Thread.interrupted()) {
            String message = textOutQueue.poll();
            if (message != null) {
                manager.sendTextMessage("17155046198", null, message, null, null);
                Log.i(TAG, String.format("Sent message: %s", message));
            }
            try {
                Thread.sleep(100); //use timeout to encourage in-order arrival TODO: fix this.
            } catch (InterruptedException e) {
            }
        }
    }
}
