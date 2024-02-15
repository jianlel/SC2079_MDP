package com.example.mdp_group31.main;

import android.Manifest;
import android.app.ProgressDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.ListView;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import com.example.mdp_group31.MainActivity;
import com.example.mdp_group31.R;

import java.util.ArrayList;
import java.util.Set;
import java.util.UUID;

public class BluetoothPopUp extends AppCompatActivity {
    private static final int PERMISSION_REQUEST_BLUETOOTH_SCAN = 1;

    private static final String TAG = "BluetoothPopUp";
    private String connStatus;
    BluetoothAdapter mBluetoothAdapter;
    public ArrayList<BluetoothDevice> mNewBTDevices;
    public ArrayList<BluetoothDevice> mPairedBTDevices;
    public DeviceListAdapter mNewDevlceListAdapter;
    public DeviceListAdapter mPairedDevlceListAdapter;
    TextView connStatusTextView;
    ListView otherDevicesListView;
    ListView pairedDevicesListView;
    Button connectBtn;
    ProgressDialog myDialog;

    SharedPreferences sharedPreferences;
    SharedPreferences.Editor editor;

    BluetoothConnectionService mBluetoothConnection;
    private static final UUID myUUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    public static BluetoothDevice mBTDevice;

    boolean retryConnection = false;
    Handler reconnectionHandler = new Handler();

    Runnable reconnectionRunnable = new Runnable() {
        @Override
        public void run() {
            // Magic here
            try {
                if (BluetoothConnectionService.BluetoothConnectionStatus == false) {
                    startBTConnection(mBTDevice, myUUID);
                    Toast.makeText(BluetoothPopUp.this, "Reconnection Success", Toast.LENGTH_SHORT).show();

                }
                reconnectionHandler.removeCallbacks(reconnectionRunnable);
                retryConnection = false;
            } catch (Exception e) {
                Toast.makeText(BluetoothPopUp.this, "Failed to reconnect, trying in 5 second", Toast.LENGTH_SHORT).show();
            }
        }
    };

    private void requestBluetoothPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            int accessFineLocationPermission = checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION);
            int accessCoarseLocationPermission = checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION);
            int bluetoothPermission = checkSelfPermission(Manifest.permission.BLUETOOTH);
            int bluetoothAdminPermission = checkSelfPermission(Manifest.permission.BLUETOOTH_ADMIN);

            ArrayList<String> permissionsList = new ArrayList<>();

            if (accessFineLocationPermission != PackageManager.PERMISSION_GRANTED) {
                permissionsList.add(Manifest.permission.ACCESS_FINE_LOCATION);
            }
            if (accessCoarseLocationPermission != PackageManager.PERMISSION_GRANTED) {
                permissionsList.add(Manifest.permission.ACCESS_COARSE_LOCATION);
            }
            if (bluetoothPermission != PackageManager.PERMISSION_GRANTED) {
                permissionsList.add(Manifest.permission.BLUETOOTH);
            }
            if (bluetoothAdminPermission != PackageManager.PERMISSION_GRANTED) {
                permissionsList.add(Manifest.permission.BLUETOOTH_ADMIN);
            }

            if (!permissionsList.isEmpty()) {
                String[] permissionsArray = new String[permissionsList.size()];
                permissionsArray = permissionsList.toArray(permissionsArray);
                requestPermissions(permissionsArray, 1); // Use any requestCode you prefer
            }
        }
    }

    private boolean checkAndRequestPermissions() {
        if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
            // request bluetooth permissions
            ActivityCompat.requestPermissions(BluetoothPopUp.this,
                    new String[]{Manifest.permission.BLUETOOTH_SCAN},
                    PERMISSION_REQUEST_BLUETOOTH_SCAN);
            return false;
        }
        else if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
            // request bluetooth permissions
            ActivityCompat.requestPermissions(BluetoothPopUp.this,
                    new String[]{Manifest.permission.BLUETOOTH_CONNECT},
                    PERMISSION_REQUEST_BLUETOOTH_SCAN);
            return false;
        }
        return true;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.bluetooth_pop_up_window);

        requestBluetoothPermissions();

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);

        int width = dm.widthPixels;
        int height = dm.heightPixels;

        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        Switch bluetoothSwitch = findViewById(R.id.bluetoothSwitch);
        if (mBluetoothAdapter.isEnabled()) {
            bluetoothSwitch.setChecked(true);
            bluetoothSwitch.setText("ON");
        }

        otherDevicesListView = findViewById(R.id.otherDevicesListView);
        pairedDevicesListView = findViewById(R.id.pairedDevicesListView);
        mNewBTDevices = new ArrayList<>();
        mPairedBTDevices = new ArrayList<>();

        connectBtn = findViewById(R.id.connectBtn);

        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_BOND_STATE_CHANGED);
        registerReceiver(mBroadcastReceiver4, filter);

        IntentFilter filter2 = new IntentFilter("ConnectionStatus");
        LocalBroadcastManager.getInstance(this).registerReceiver(mBroadcastReceiver5, filter2);

        otherDevicesListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
                    // request bluetooth permissions
                    ActivityCompat.requestPermissions(BluetoothPopUp.this,
                            new String[]{Manifest.permission.BLUETOOTH_SCAN},
                            PERMISSION_REQUEST_BLUETOOTH_SCAN);
                    return;
                }
                if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                    // request bluetooth permissions
                    ActivityCompat.requestPermissions(BluetoothPopUp.this,
                            new String[]{Manifest.permission.BLUETOOTH_CONNECT},
                            PERMISSION_REQUEST_BLUETOOTH_SCAN);
                    return;
                }
                mBluetoothAdapter.cancelDiscovery();
                pairedDevicesListView.setAdapter(mPairedDevlceListAdapter);

                String deviceName = mNewBTDevices.get(i).getName();
                String deviceAddress = mNewBTDevices.get(i).getAddress();
                Log.d(TAG, "onItemClick: A device is selected.");
                Log.d(TAG, "onItemClick: DEVICE NAME: " + deviceName);
                Log.d(TAG, "onItemClick: DEVICE ADDRESS: " + deviceAddress);

                if (Build.VERSION.SDK_INT > Build.VERSION_CODES.JELLY_BEAN_MR2) {
                    Log.d(TAG, "onItemClick: Initiating pairing with " + deviceName);
                    mNewBTDevices.get(i).createBond();

                    mBluetoothConnection = new BluetoothConnectionService(BluetoothPopUp.this);
                    mBTDevice = mNewBTDevices.get(i);
                }
            }
        });

        pairedDevicesListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
                    // request bluetooth permissions
                    ActivityCompat.requestPermissions(BluetoothPopUp.this,
                            new String[]{Manifest.permission.BLUETOOTH_SCAN},
                            PERMISSION_REQUEST_BLUETOOTH_SCAN);
                    return;
                }
                if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                    // request bluetooth permissions
                    ActivityCompat.requestPermissions(BluetoothPopUp.this,
                            new String[]{Manifest.permission.BLUETOOTH_CONNECT},
                            PERMISSION_REQUEST_BLUETOOTH_SCAN);
                    return;
                }
                mBluetoothAdapter.cancelDiscovery();
                otherDevicesListView.setAdapter(mNewDevlceListAdapter);

                String deviceName = mPairedBTDevices.get(i).getName();
                String deviceAddress = mPairedBTDevices.get(i).getAddress();
                Log.d(TAG, "onItemClick: A device is selected.");
                Log.d(TAG, "onItemClick: DEVICE NAME: " + deviceName);
                Log.d(TAG, "onItemClick: DEVICE ADDRESS: " + deviceAddress);

                mBluetoothConnection = new BluetoothConnectionService(BluetoothPopUp.this);
                mBTDevice = mPairedBTDevices.get(i);
            }
        });

        bluetoothSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean isChecked) {
                Log.d(TAG, "onChecked: Switch button toggled. Enabling/Disabling Bluetooth");
                if(isChecked){
                    compoundButton.setText("ON");
                }else
                {
                    compoundButton.setText("OFF");
                }

                if(mBluetoothAdapter ==null){
                    Log.d(TAG, "enableDisableBT: Device does not support Bluetooth capabilities!");
                    Toast.makeText(BluetoothPopUp.this, "Device Does Not Support Bluetooth capabilities!", Toast.LENGTH_SHORT).show();
                    compoundButton.setChecked(false);
                }
                else {
                    if (!mBluetoothAdapter.isEnabled()) {
                        Log.d(TAG, "enableDisableBT: enabling Bluetooth");
                        Log.d(TAG, "enableDisableBT: Making device discoverable for 600 seconds.");

                        if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
                            // request bluetooth permissions
                            ActivityCompat.requestPermissions(BluetoothPopUp.this,
                                    new String[]{Manifest.permission.BLUETOOTH_SCAN},
                                    PERMISSION_REQUEST_BLUETOOTH_SCAN);
                            return;
                        }
                        if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                            // request bluetooth permissions
                            ActivityCompat.requestPermissions(BluetoothPopUp.this,
                                    new String[]{Manifest.permission.BLUETOOTH_CONNECT},
                                    PERMISSION_REQUEST_BLUETOOTH_SCAN);
                            return;
                        }
                        Intent discoverableIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE);
                        discoverableIntent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 300);
                        startActivity(discoverableIntent);

                        compoundButton.setChecked(true);

                        IntentFilter BTIntent = new IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED);
                        registerReceiver(mBroadcastReceiver1, BTIntent);

                        IntentFilter discoverIntent = new IntentFilter(BluetoothAdapter.ACTION_SCAN_MODE_CHANGED);
                        registerReceiver(mBroadcastReceiver2, discoverIntent);
                    }
                    if (mBluetoothAdapter.isEnabled()) {
                        Log.d(TAG, "enableDisableBT: disabling Bluetooth");
                        mBluetoothAdapter.disable();

                        IntentFilter BTIntent = new IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED);
                        registerReceiver(mBroadcastReceiver1, BTIntent);
                    }
                }
            }
        });

        connectBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(mBTDevice ==null)
                {
                    Toast.makeText(BluetoothPopUp.this, "Please Select a Device before connecting.", Toast.LENGTH_SHORT).show();
                }
                else {
                    startConnection();
                }
            }
        });


        Button backBtn = findViewById(R.id.backBtn);

        connStatusTextView = findViewById(R.id.connStatusTextView);
        connStatus ="Disconnected";
        sharedPreferences = getApplicationContext().getSharedPreferences("Shared Preferences", Context.MODE_PRIVATE);
        if (sharedPreferences.contains("connStatus"))
            connStatus = sharedPreferences.getString("connStatus", "");

        connStatusTextView.setText(connStatus);

        backBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                editor = sharedPreferences.edit();
                editor.putString("connStatus", connStatusTextView.getText().toString());
                editor.commit();
                TextView status = MainActivity.getBluetoothStatus();
                String s = connStatusTextView.getText().toString();
                //status.setText(s);
                finish();
            }
        });

        myDialog = new ProgressDialog(BluetoothPopUp.this);
        myDialog.setMessage("Waiting for other device to reconnect...");
        myDialog.setCancelable(false);
        myDialog.setButton(DialogInterface.BUTTON_NEGATIVE, "Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        if (requestCode == PERMISSION_REQUEST_BLUETOOTH_SCAN) {
            // Check if the permission is granted
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permission granted, you can proceed with Bluetooth operations
            } else {
                // Permission denied, inform the user or take appropriate action
                Toast.makeText(BluetoothPopUp.this, "Bluetooth scan permission denied", Toast.LENGTH_SHORT).show();
            }
        }
    }

    public void Scanning(){
        Log.d(TAG, "toggleButton: Scanning for unpaired devices...");
        if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
            // request bluetooth permissions
            ActivityCompat.requestPermissions(BluetoothPopUp.this,
                    new String[]{Manifest.permission.BLUETOOTH_SCAN},
                    PERMISSION_REQUEST_BLUETOOTH_SCAN);
            return;
        }
        if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
            // request bluetooth permissions
            ActivityCompat.requestPermissions(BluetoothPopUp.this,
                    new String[]{Manifest.permission.BLUETOOTH_CONNECT},
                    PERMISSION_REQUEST_BLUETOOTH_SCAN);
            return;
        }
        mNewBTDevices.clear();
        if(mBluetoothAdapter != null) {
            if (!mBluetoothAdapter.isEnabled()) {
                Toast.makeText(BluetoothPopUp.this, "Please turn on Bluetooth first!", Toast.LENGTH_SHORT).show();
            }
            if (mBluetoothAdapter.isDiscovering()) {
                mBluetoothAdapter.cancelDiscovery();

                checkBTPermissions();

                mBluetoothAdapter.startDiscovery();
                IntentFilter discoverDevicesIntent = new IntentFilter(BluetoothDevice.ACTION_FOUND);
                registerReceiver(mBroadcastReceiver3, discoverDevicesIntent);
            } else if (!mBluetoothAdapter.isDiscovering()) {
                Log.d("bluetooth", "Checking bluetooth permissions");
                checkBTPermissions();

                mBluetoothAdapter.startDiscovery();
                IntentFilter discoverDevicesIntent = new IntentFilter(BluetoothDevice.ACTION_FOUND);
                registerReceiver(mBroadcastReceiver3, discoverDevicesIntent);
            }
            mPairedBTDevices.clear();
            Log.d(TAG, "cleared bt device");
            Set<BluetoothDevice> pairedDevices;
            try {
            Log.d(TAG, "getting bonded device "+ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_CONNECT));
            pairedDevices = mBluetoothAdapter.getBondedDevices();
            Log.d(TAG, "worked");

            Log.d(TAG, "toggleButton: Number of paired devices found: "+ pairedDevices.size());
            for(BluetoothDevice d : pairedDevices){
                Log.d(TAG, "Paired Devices: "+ d.getName() +" : " + d.getAddress());
                mPairedBTDevices.add(d);
                mPairedDevlceListAdapter = new DeviceListAdapter(this, R.layout.device_adapter_view, mPairedBTDevices);
                pairedDevicesListView.setAdapter(mPairedDevlceListAdapter);
            }
            } catch(Exception e) {
                e.printStackTrace();
            }
        }

    }

    public void toggleButtonScan(View view){
        Log.d("control", "tapped on toggle scan button");
        Scanning();
    }

    private void checkBTPermissions() {
        if(Build.VERSION.SDK_INT > Build.VERSION_CODES.LOLLIPOP){
            int permissionCheck = this.checkSelfPermission("Manifest.permission.ACCESS_FINE_LOCATION");
            permissionCheck += this.checkSelfPermission("Manifest.permission.ACCESS_COARSE_LOCATION");
            if (permissionCheck != 0) {
                this.requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, 1001);
            }
        } else {
            Log.d(TAG, "checkBTPermissions: No need to check permissions. SDK version < LOLLIPOP.");
        }
    }

    private final BroadcastReceiver mBroadcastReceiver1 = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if (action.equals(BluetoothAdapter.ACTION_STATE_CHANGED)) {
                final int state = intent.getIntExtra(BluetoothAdapter.EXTRA_STATE, BluetoothAdapter.ERROR);

                switch (state) {
                    case BluetoothAdapter.STATE_OFF:
                        Log.d(TAG, "mBroadcastReceiver1: STATE OFF");
                        break;
                    case BluetoothAdapter.STATE_TURNING_OFF:
                        Log.d(TAG, "mBroadcastReceiver1: STATE TURNING OFF");
                        break;
                    case BluetoothAdapter.STATE_ON:
                        Log.d(TAG, "mBroadcastReceiver1: STATE ON");

                        break;
                    case BluetoothAdapter.STATE_TURNING_ON:
                        Log.d(TAG, "mBroadcastReceiver1: STATE TURNING ON");
                        break;
                }
            }
        }
    };

    private final BroadcastReceiver mBroadcastReceiver2 = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if (action.equals(BluetoothAdapter.ACTION_SCAN_MODE_CHANGED)) {
                final int mode = intent.getIntExtra(BluetoothAdapter.EXTRA_SCAN_MODE, BluetoothAdapter.ERROR);

                switch (mode) {
                    case BluetoothAdapter.SCAN_MODE_CONNECTABLE_DISCOVERABLE:
                        Log.d(TAG, "mBroadcastReceiver2: Discoverability Enabled.");
                        break;
                    case BluetoothAdapter.SCAN_MODE_CONNECTABLE:
                        Log.d(TAG, "mBroadcastReceiver2: Discoverability Disabled. Able to receive connections.");
                        break;
                    case BluetoothAdapter.SCAN_MODE_NONE:
                        Log.d(TAG, "mBroadcastReceiver2: Discoverability Disabled. Not able to receive connections.");
                        break;
                    case BluetoothAdapter.STATE_CONNECTING:
                        Log.d(TAG, "mBroadcastReceiver2: Connecting...");
                        break;
                    case BluetoothAdapter.STATE_CONNECTED:
                        Log.d(TAG, "mBroadcastReceiver2: Connected.");
                        break;
                }
            }
        }
    };

    private final BroadcastReceiver mBroadcastReceiver3 = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
                // request bluetooth permissions
                ActivityCompat.requestPermissions(BluetoothPopUp.this,
                        new String[]{Manifest.permission.BLUETOOTH_SCAN},
                        PERMISSION_REQUEST_BLUETOOTH_SCAN);
                return;
            }
            if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                // request bluetooth permissions
                ActivityCompat.requestPermissions(BluetoothPopUp.this,
                        new String[]{Manifest.permission.BLUETOOTH_CONNECT},
                        PERMISSION_REQUEST_BLUETOOTH_SCAN);
                return;
            }
            final String action = intent.getAction();
            Log.d(TAG, "onReceive: ACTION FOUND.");

            if(action.equals(BluetoothDevice.ACTION_FOUND)) {
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                if(device.getBondState()!=BluetoothDevice.BOND_BONDED) {
                    mNewBTDevices.add(device);
                    Log.d(TAG, "onReceive: " + device.getName() + " : " + device.getAddress());
                    mNewDevlceListAdapter = new DeviceListAdapter(context, R.layout.device_adapter_view, mNewBTDevices);
                    otherDevicesListView.setAdapter(mNewDevlceListAdapter);
                }
            }
        }
    };

    private final BroadcastReceiver mBroadcastReceiver4 = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
                // request bluetooth permissions
                ActivityCompat.requestPermissions(BluetoothPopUp.this,
                        new String[]{Manifest.permission.BLUETOOTH_SCAN},
                        PERMISSION_REQUEST_BLUETOOTH_SCAN);
                return;
            }
            if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                // request bluetooth permissions
                ActivityCompat.requestPermissions(BluetoothPopUp.this,
                        new String[]{Manifest.permission.BLUETOOTH_CONNECT},
                        PERMISSION_REQUEST_BLUETOOTH_SCAN);
                return;
            }
            final String action = intent.getAction();

            if(action.equals(BluetoothDevice.ACTION_BOND_STATE_CHANGED)){
                BluetoothDevice mDevice = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                if(mDevice.getBondState() == BluetoothDevice.BOND_BONDED){
                    Log.d(TAG, "BOND_BONDED.");
                    Toast.makeText(BluetoothPopUp.this, "Successfully paired with " + mDevice.getName(), Toast.LENGTH_SHORT).show();
                    mBTDevice = mDevice;
                    Scanning();


                }
                if(mDevice.getBondState() == BluetoothDevice.BOND_BONDING){
                    Log.d(TAG, "BOND_BONDING.");
                }
                if(mDevice.getBondState() == BluetoothDevice.BOND_NONE){
                    Log.d(TAG, "BOND_NONE.");
                }
            }
        }
    };

    private final BroadcastReceiver mBroadcastReceiver5 = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
                // request bluetooth permissions
                ActivityCompat.requestPermissions(BluetoothPopUp.this,
                        new String[]{Manifest.permission.BLUETOOTH_SCAN},
                        PERMISSION_REQUEST_BLUETOOTH_SCAN);
                return;
            }
            if (ActivityCompat.checkSelfPermission(BluetoothPopUp.this, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                // request bluetooth permissions
                ActivityCompat.requestPermissions(BluetoothPopUp.this,
                        new String[]{Manifest.permission.BLUETOOTH_CONNECT},
                        PERMISSION_REQUEST_BLUETOOTH_SCAN);
                return;
            }
            BluetoothDevice mDevice = intent.getParcelableExtra("Device");
            String status = intent.getStringExtra("Status");
            sharedPreferences = getApplicationContext().getSharedPreferences("Shared Preferences", Context.MODE_PRIVATE);
            editor = sharedPreferences.edit();

            if(status.equals("connected")){
                try {
                    myDialog.dismiss();
                } catch(NullPointerException e){
                    e.printStackTrace();
                }

                Log.d(TAG, "mBroadcastReceiver5: Device now connected to "+mDevice.getName());
                Toast.makeText(BluetoothPopUp.this, "Device now connected to "+mDevice.getName(), Toast.LENGTH_SHORT).show();
                editor.putString("connStatus", "Connected to " + mDevice.getName());
                connStatusTextView.setText("Connected to " + mDevice.getName());

            }
            else if(status.equals("disconnected") && retryConnection == false){
                Log.d(TAG, "mBroadcastReceiver5: Disconnected from "+mDevice.getName());
                Toast.makeText(BluetoothPopUp.this, "Disconnected from "+mDevice.getName(), Toast.LENGTH_SHORT).show();
                mBluetoothConnection = new BluetoothConnectionService(BluetoothPopUp.this);
//                mBluetoothConnection.startAcceptThread();


                sharedPreferences = getApplicationContext().getSharedPreferences("Shared Preferences", Context.MODE_PRIVATE);
                editor = sharedPreferences.edit();
                editor.putString("connStatus", "Disconnected");
                TextView connStatusTextView = findViewById(R.id.connStatusTextView);
                connStatusTextView.setText("Disconnected");

                editor.commit();

                try {
                    myDialog.show();
                }catch (Exception e){
                    Log.d(TAG, "BluetoothPopUp: mBroadcastReceiver5 Dialog show failure");
                }
                retryConnection = true;
                reconnectionHandler.postDelayed(reconnectionRunnable, 5000);

            }
            editor.commit();
        }
    };

    public void startConnection(){
        startBTConnection(mBTDevice,myUUID);
    }

    public void startBTConnection(BluetoothDevice device, UUID uuid){
        Log.d(TAG, "startBTConnection: Initializing RFCOM Bluetooth Connection");
        mBluetoothConnection.startClientThread(device, uuid);
    }

    @Override
    protected void onDestroy() {
        Log.d(TAG, "onDestroy: called");
        super.onDestroy();
        try {
            unregisterReceiver(mBroadcastReceiver1);
            unregisterReceiver(mBroadcastReceiver2);
            unregisterReceiver(mBroadcastReceiver3);
            unregisterReceiver(mBroadcastReceiver4);
            LocalBroadcastManager.getInstance(this).unregisterReceiver(mBroadcastReceiver5);
        } catch(IllegalArgumentException e){
            e.printStackTrace();
        }
    }

    @Override
    protected void onPause() {
        Log.d(TAG, "onPause: called");
        super.onPause();
        try {
            if (mBroadcastReceiver1 != null) {
                unregisterReceiver(mBroadcastReceiver1);
            }
            if (mBroadcastReceiver2 != null) {
                unregisterReceiver(mBroadcastReceiver2);
            }
            if (mBroadcastReceiver3 != null) {
                unregisterReceiver(mBroadcastReceiver3);
            }
            if (mBroadcastReceiver4 != null) {
                unregisterReceiver(mBroadcastReceiver4);
            }
            if (mBroadcastReceiver5 != null) {
                LocalBroadcastManager.getInstance(this).unregisterReceiver(mBroadcastReceiver5);
            }
        } catch(IllegalArgumentException e){
            e.printStackTrace();
        }
    }

    @Override
    public void finish() {
        Intent data = new Intent();
        data.putExtra("mBTDevice", mBTDevice);
        data.putExtra("myUUID",myUUID);
        setResult(RESULT_OK, data);
        super.finish();
    }
}
