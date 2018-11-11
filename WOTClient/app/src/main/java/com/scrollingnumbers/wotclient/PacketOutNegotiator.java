/*
 ** Copyright 2015, Mohamed Naufal
 **
 ** Licensed under the Apache License, Version 2.0 (the "License");
 ** you may not use this file except in compliance with the License.
 ** You may obtain a copy of the License at
 **
 **     http://www.apache.org/licenses/LICENSE-2.0
 **
 ** Unless required by applicable law or agreed to in writing, software
 ** distributed under the License is distributed on an "AS IS" BASIS,
 ** WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 ** See the License for the specific language governing permissions and
 ** limitations under the License.
 */


package com.scrollingnumbers.wotclient;

import android.content.res.Resources;
import android.util.Log;

import java.io.IOException;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.concurrent.Callable;
import java.util.concurrent.ConcurrentLinkedQueue;

class PacketOutNegotiator implements Runnable {
    public static final String TAG = PacketOutNegotiator.class.getSimpleName();

    private ConcurrentLinkedQueue<Packet> packetOutQueue;
    private ConcurrentLinkedQueue<ByteBuffer> packetInQueue;
    private ConcurrentLinkedQueue<String> textOutQueue;

    private String outputText;

    public PacketOutNegotiator(ConcurrentLinkedQueue packetOutQueue, ConcurrentLinkedQueue textOutQueue, ConcurrentLinkedQueue packetInQueue) {
        this.packetOutQueue = packetOutQueue;
        this.textOutQueue = textOutQueue;
        this.packetInQueue = packetInQueue;
    }

    @Override
    public void run() {
        while (!Thread.interrupted()) {

        }
    }
}
