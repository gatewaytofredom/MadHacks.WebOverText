package com.scrollingnumbers.wotclient;

import android.Manifest;
import android.app.Service;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.IBinder;
import android.provider.Telephony;
import android.support.v4.content.ContextCompat;
import android.util.Log;

public class SMSService extends Service {

    SMSReceiver receiver;
    IntentFilter intentFilter;

    @Override
    public void onCreate() {
        super.onCreate();

        Log.i("SMSService", "start");
        //Log.i("SMSService", Integer.toString(ContextCompat.checkSelfPermission(this, Manifest.permission.READ_SMS)));

        receiver = new SMSReceiver();
        intentFilter = new IntentFilter();

        Log.i("SMSService", Telephony.Sms.Intents.SMS_RECEIVED_ACTION);
        intentFilter.addAction(Telephony.Sms.Intents.SMS_RECEIVED_ACTION);
        registerReceiver(receiver, intentFilter);
    }

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        unregisterReceiver(receiver);
    }

}
