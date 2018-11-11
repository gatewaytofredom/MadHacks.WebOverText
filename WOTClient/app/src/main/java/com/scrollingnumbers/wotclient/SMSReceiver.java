package com.scrollingnumbers.wotclient;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.telephony.SmsMessage;
import android.util.Log;

public class SMSReceiver extends BroadcastReceiver {

    private final String TAG = this.getClass().getSimpleName();

    public SMSReceiver() {Log.i(TAG, "START");}

    @Override
    public void onReceive(Context context, Intent intent) {
        Bundle extras = intent.getExtras();
        Log.i(TAG, "wah");

        if (extras != null) {
            byte[][] smsextrass = (byte[][])extras.get("pdus");
            for (int i = 0; i < smsextrass.length; i++) {
                SmsMessage msg = SmsMessage.createFromPdu(smsextrass[i]);
                Log.i(TAG, String.format(
                        "Recv'd msg: %s, %s",
                        msg.getOriginatingAddress(),
                        msg.getMessageBody().toString())
                );

                SmsManager manager = SmsManager.getDefault();
                manager.sendTextMessage(msg.getOriginatingAddress(), null ,"*Dabs*", null, null);
            }
        }
    }
}
