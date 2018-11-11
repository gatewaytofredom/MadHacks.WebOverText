package com.scrollingnumbers.wotclient;

import java.util.concurrent.Callable;
import java.util.concurrent.ConcurrentLinkedQueue;

class PacketInNegotiator implements Runnable {
    public static final String TAG = PacketInNegotiator.class.getSimpleName();

    private ConcurrentLinkedQueue<String> textInQueue;


    public PacketInNegotiator(ConcurrentLinkedQueue textInQueue, ConcurrentLinkedQueue packetInQueue) {
    }

    @Override
    public void run() {

    }
}
