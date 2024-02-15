package com.example.mdp_group31.main;

import static com.example.mdp_group31.R.id.sendObsBtn;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import com.example.mdp_group31.MainActivity;
import com.example.mdp_group31.R;

import java.util.Arrays;
import java.util.Locale;

/**
 * ControlFragment is a Fragment class that displays the control buttons and timers for the robot in the
 * MainActivity.

 * It contains two timers for image recognition and fastest car simulation, and button listeners
 * to control the robot's movement.
 */
public class ControlFragment extends Fragment {
    /**
     * A string constant used for logging purposes.
     */
    private static final String TAG = "ControlFragment";
    /**
     * The MainActivity instance that contains this fragment.
     */
    private final MainActivity mainActivity;

    private long imgRecTime, fastestCarTime;
    private SharedPreferences sharedPreferences;
    private ToggleButton imgRecBtn, fastestCarBtn;
    private TextView imgRecText, fastestCarText, robotStatusText;
    private GridMap gridMap;
    private int[] curCoord;
    private String direction;

    /**
     * Creates an instance of ControlFragment with the specified MainActivity instance.
     *
     * @param main the MainActivity instance that contains this fragment
     */
    public ControlFragment(MainActivity main) {
        this.mainActivity = main;
    }

    /**
     * The Handler used for timing the image recognition timer and fastest car timer.
     */
    public static Handler timerHandler = new Handler();

    /**
     * The Runnable for the image recognition timer.
     */
    public Runnable imgRecTimer = new Runnable() {
        @Override
        public void run() {
            long msTime = System.currentTimeMillis() - imgRecTime;
            int sTime = (int) (msTime / 1000);
            int minuteTime = sTime / 60;
            sTime = sTime % 60;

            if (! mainActivity.imgRecTimerFlag) {
                imgRecText.setText(String.format(Locale.US, "%02d:%02d", minuteTime, sTime));
                timerHandler.postDelayed(this, 500);
            }
        }
    };

    /**
     * The Runnable for the fastest car timer.
     */
    public Runnable fastestCarTimer = new Runnable() {
        @Override
        public void run() {
            long msTime = System.currentTimeMillis() - fastestCarTime;
            int sTime = (int) (msTime / 1000);
            int minuteTime = sTime / 60;
            sTime = sTime % 60;

            if (!mainActivity.fastestCarTimerFlag) {
                fastestCarText.setText(String.format(Locale.US,"%02d:%02d", minuteTime,
                        sTime));
                timerHandler.postDelayed(this, 500);
            }
        }
    };

    /**
     * Initializes the fragment.
     *
     * @param savedInstanceState the saved instance state
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    /**
     * Creates and returns the view hierarchy associated with the fragment.
     *
     * @param inflater           the LayoutInflater object that can be used to inflate any views in the fragment
     * @param container          the parent view that the fragment's UI should be attached to
     * @param savedInstanceState the saved instance state
     * @return the View for the fragment's UI, or null
     */
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // inflate
        View root = inflater.inflate(R.layout.activity_control, container, false);

        // get shared preferences
        this.sharedPreferences = requireActivity()
                .getSharedPreferences("Shared Preferences", Context.MODE_PRIVATE);

        // initialize all buttons and text views
        ImageButton forwardBtn = this.mainActivity.getUpBtn();
        ImageButton rightUpBtn = this.mainActivity.getRightUpBtn();
        ImageButton backBtn = this.mainActivity.getDownBtn();
        ImageButton leftUpBtn = this.mainActivity.getLeftUpBtn();
        ImageButton leftDownBtn = this.mainActivity.getLeftDownBtn();
        ImageButton rightDownBtn = this.mainActivity.getRightDownBtn();
        ImageButton imgRecResetBtn = root.findViewById(R.id.exploreResetImageBtn2);
        Button sendObsBtn = root.findViewById(R.id.sendObsBtn);
        ImageButton fastestCarResetBtn = root.findViewById(R.id.fastestResetImageBtn2);
        this.imgRecText = root.findViewById(R.id.exploreTimeTextView2);
        this.fastestCarText = root.findViewById(R.id.fastestTimeTextView2);
        this.imgRecBtn = root.findViewById(R.id.exploreToggleBtn2);
        this.fastestCarBtn = root.findViewById(R.id.fastestToggleBtn2);
        this.robotStatusText = this.mainActivity.getRobotStatusText();

        // default time is 0
        this.fastestCarTime = 0;
        this.imgRecTime = 0;

        // need to get the gridMap to call the private methods
        this.gridMap = this.mainActivity.getGridMap();

        // button listeners. Runs when the buttons are pressed
        forwardBtn.setOnClickListener(view -> {
            // only reacts when robot is placed on gridmap
            if (this.gridMap.getCanDrawRobot()) {
                this.curCoord = this.gridMap.getCurCoord();
                this.direction = this.gridMap.getRobotDirection();
                // handles translation based on robot direction
                int[] newCoord = new int[2];
                switch (this.direction) {
                    case "up":
                        newCoord =new int[]{this.curCoord[0], this.curCoord[1]+1};
                        break;
                    case "left":
                        newCoord = new int[]{this.curCoord[0] - 1, this.curCoord[1]};
                        break;
                    case "down":
                        newCoord = new int[]{this.curCoord[0], this.curCoord[1] - 1};
                        break;
                    case "right":
                        newCoord = new int[]{this.curCoord[0] + 1, this.curCoord[1]};
                        break;
                }

                if(!areObstaclesInFront(newCoord)) {
                    this.gridMap.moveRobot(newCoord, 0);
                    this.mainActivity.refreshCoordinate();
                }
            }
            else
                this.showToast("Please place robot on map to begin");
        });

        rightUpBtn.setOnClickListener(view -> {
            if (this.gridMap.getCanDrawRobot()) {
                this.curCoord = this.gridMap.getCurCoord();
                this.direction = this.gridMap.getRobotDirection(); // robot direction
                int newCoord[] = null;
                switch (this.direction) {
                    case "up":
                        newCoord = new int[]{this.curCoord[0] + 3, this.curCoord[1] + 1};
                        break;
                    case "left":
                        newCoord = new int[]{this.curCoord[0] - 1, this.curCoord[1] + 3};
                        break;
                    case "down":
                        newCoord = new int[]{this.curCoord[0] - 3, this.curCoord[1] - 1};
                        break;
                    case "right":
                        newCoord = new int[]{this.curCoord[0] + 1, this.curCoord[1] - 3};
                        break;
                }

                if(!areObstaclesInFront(newCoord)) {
                    this.gridMap.moveRobot(newCoord, -90);
                    this.mainActivity.refreshCoordinate();
                }
            }
            else
                this.showToast("Please place robot on map to begin");
        });

        rightDownBtn.setOnClickListener(view -> {
            if (this.gridMap.getCanDrawRobot()) {
                this.curCoord = this.gridMap.getCurCoord();
                this.direction = this.gridMap.getRobotDirection(); // robot direction
                int newCoord[] = null;
                switch (this.direction) {
                    case "up":
                        newCoord = new int[]{this.curCoord[0] + 3, this.curCoord[1] - 1};
                        break;
                    case "left":
                        newCoord = new int[]{this.curCoord[0] + 1, this.curCoord[1] + 3};
                        break;
                    case "down":
                        newCoord = new int[]{this.curCoord[0] - 3, this.curCoord[1] + 1};
                        break;
                    case "right":
                        newCoord = new int[]{this.curCoord[0] - 1, this.curCoord[1] - 3};
                        break;
                }

                if(!areObstaclesInFront(newCoord)) {
                    this.gridMap.moveRobot(newCoord, 90);
                    this.mainActivity.refreshCoordinate();
                }
            }
            else
                this.showToast("Please place robot on map to begin");
        });

        backBtn.setOnClickListener(view -> {
            if (this.gridMap.getCanDrawRobot()) {
                this.curCoord = this.gridMap.getCurCoord();
                this.direction = this.gridMap.getRobotDirection();
                int[] newCoord = null;
                switch (this.direction) { // robot direction
                    case "up":
                        newCoord = new int[]{this.curCoord[0], this.curCoord[1] - 1};
                        break;
                    case "left":
                        newCoord = new int[]{this.curCoord[0] + 1, this.curCoord[1]};
                        break;
                    case "down":
                        newCoord = new int[]{this.curCoord[0], this.curCoord[1] + 1};
                        break;
                    case "right":
                        newCoord = new int[]{this.curCoord[0] - 1, this.curCoord[1]};
                        break;
                }
                if(!areObstaclesInFront(newCoord)) {
                    this.gridMap.moveRobot(newCoord, 0);
                    this.mainActivity.refreshCoordinate();
                }
            }
            else {
                this.showToast("Please place robot on map to begin");
            }
        });

        leftUpBtn.setOnClickListener(view -> {
            if (this.gridMap.getCanDrawRobot()) {
                this.curCoord = this.gridMap.getCurCoord();
                this.direction = this.gridMap.getRobotDirection(); // robot direction
                int[] newCoord = null;
                switch (this.direction) {
                    case "up":
                        newCoord = new int[]{this.curCoord[0] - 3, this.curCoord[1] + 1};
                        break;
                    case "left":
                        newCoord = new int[]{this.curCoord[0] - 1, this.curCoord[1] - 3};
                        break;
                    case "down":
                        newCoord = new int[]{this.curCoord[0] + 3, this.curCoord[1] - 1};
                        break;
                    case "right":
                        newCoord = new int[]{this.curCoord[0] + 1, this.curCoord[1] + 3};
                        break;
                }
                if(!areObstaclesInFront(newCoord)) {
                    this.gridMap.moveRobot(newCoord, 90);
                    this.mainActivity.refreshCoordinate();
                }
            }
            else
                this.showToast("Please place robot on map to begin");
        });

        leftDownBtn.setOnClickListener(view -> {
            if (this.gridMap.getCanDrawRobot()) {
                this.curCoord = this.gridMap.getCurCoord();
                this.direction = this.gridMap.getRobotDirection(); // robot direction
                int[] newCoord = null;
                switch (this.direction) {
                    case "up":
                        newCoord = new int[]{this.curCoord[0] - 3, this.curCoord[1] - 1};
                        break;
                    case "left":
                        newCoord = new int[]{this.curCoord[0] + 1, this.curCoord[1] - 3};
                        break;
                    case "down":
                        newCoord = new int[]{this.curCoord[0] + 3, this.curCoord[1] + 1};
                        break;
                    case "right":
                        newCoord = new int[]{this.curCoord[0] - 1, this.curCoord[1] + 3};
                        break;
                }
                if(!areObstaclesInFront(newCoord)) {
                    this.gridMap.moveRobot(newCoord, 270);
                    this.mainActivity.refreshCoordinate();
                }
            }
            else
                this.showToast("Please place robot on map to begin");
        });

        sendObsBtn.setOnClickListener(v -> {
            // sending obstacles;
            String getObsPos = this.gridMap.getAllObstacles();
            Log.d("obs", getObsPos);
            this.mainActivity.sendMessage(getObsPos);
        });

        this.imgRecBtn.setOnClickListener(v -> {
            // changed from STOP to START (i.e. done with challenge)
            if (this.imgRecBtn.getText().equals("START")) {
                this.showToast("Image Recognition Completed!!");
                this.robotStatusText.setText(R.string.img_rec_stop);
                timerHandler.removeCallbacks(this.imgRecTimer);
            }
            // changed from START to STOP (i.e. started challenge)
            else if (this.imgRecBtn.getText().equals("STOP")) {
                this.mainActivity.imgRecTimerFlag = false;
                this.showToast("Image Recognition Started!!");
                String startmovementtr= "{\"cat\": \"control\", \"value\": \"start\"}";
                // sending obstacles;
                this.mainActivity.sendMessage(startmovementtr);
                this.robotStatusText.setText(R.string.img_rec_start);
                this.imgRecTime = System.currentTimeMillis();
                timerHandler.postDelayed(imgRecTimer, 0);
            }
        });

        this.fastestCarBtn.setOnClickListener(v -> {
            // changed from STOP to START (i.e., challenge completed)
            if (this.fastestCarBtn.getText().equals("START")) {
                this.showToast("Fastest Car Stopped!");
                this.robotStatusText.setText(R.string.fastest_car_stop);
                timerHandler.removeCallbacks(fastestCarTimer);
            }
            // changed from START to STOP (i.e., challenge started)
            else if (fastestCarBtn.getText().equals("STOP")) {
                this.showToast("Fastest Car started!");
                String startmovementtr= "{\"cat\": \"control\", \"value\": \"start\"}";
                this.mainActivity.sendMessage(startmovementtr);
                this.mainActivity.fastestCarTimerFlag = false;
                this.robotStatusText.setText(R.string.fastest_car_start);
                this.fastestCarTime = System.currentTimeMillis();
                timerHandler.postDelayed(fastestCarTimer, 0);
            }
        });

        imgRecResetBtn.setOnClickListener(v -> {
            this.showToast("Resetting image recognition challenge timer...");
            this.imgRecText.setText(R.string.timer_default_val);
            this.robotStatusText.setText(R.string.robot_status_na);
            if (this.imgRecBtn.isChecked())
                this.imgRecBtn.toggle();
            timerHandler.removeCallbacks(imgRecTimer);
        });

        fastestCarResetBtn.setOnClickListener(view -> {
            this.showToast("Resetting fastest car challenge timer...");
            this.fastestCarText.setText(R.string.timer_default_val);
            this.robotStatusText.setText(R.string.robot_status_na);
            if (this.fastestCarBtn.isChecked()){
                this.fastestCarBtn.toggle();
            }
            timerHandler.removeCallbacks(fastestCarTimer);
        });

        return root;
    }


    private boolean areObstaclesInFront(int[] newCoord) {

        Log.d("newCoord", newCoord[0] + " " + newCoord[1]);
        for (int i = 0; i < gridMap.getObstacleCoord().size(); i ++) {
            int[] currentObstacle = gridMap.getObstacleCoord().get(i);
            if (currentObstacle[0] <= newCoord[0] + 1 && currentObstacle[0] >= newCoord[0] - 1 && currentObstacle[1] <= newCoord[1] + 1 && currentObstacle[1] >= newCoord[1] - 1) {
                Log.d("Moving robot", "There's a obstacle." + currentObstacle[0] + " " + currentObstacle[1]);
                return true;
            }
        }

        return false;
    }

    /**
     * Method to display debug message
     * @param message The custom message shown in debugging
     */
    private void debugMessage(String message) {
        Log.d(TAG, message);
    }

    /**
     * Displays a toast with message on the UI
     * @param message The displayed message
     */
    private void showToast(String message) {
        Toast.makeText(getContext(), message, Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onDestroy(){
        super.onDestroy();
    }
}