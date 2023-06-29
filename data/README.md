### Dataset for CNN-based position estimation of soft robot end-effector

motion/  - directory of motion data collected in simulation
image/   - directory of soft robot images rendered form the motion data

There are 513 images and 513 corresponding end-effector positions.

Goal: train a convolutional neural network to map image -> xyz position of end-effector.

#### Hint to load the dataset of end-effector positions
```
motion_data = np.load(motion_data_path)
tip_pos = motion_data['position_rod1'][:, [2, 0, 1], -1]  # all positions of last node ([2,0,1] converts to xyz)
```

tip_pos has shape (n_samples, 3), with n_samples=513.



