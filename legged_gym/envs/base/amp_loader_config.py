import os


# AMP loader
from legged_gym.utils.amp.motion_loader import AMPLoader


class AMPLoaderConfig:
    def __init__(self, cfg, legged_gym_root_dir, device, time_between_frames):

        self.legged_gym_root_dir = legged_gym_root_dir
        self.files_path, self.files_names = self.get_motion_path(cfg)

        if len(cfg.env.selected_motion_names) > 0:
            filtered_files = [
                (f, n) for f, n in zip(self.files_path, self.files_names)
                if any(selected_name == n for selected_name in cfg.env.selected_motion_names)]
            
            self.files_path, self.files_names = zip(*filtered_files) if filtered_files else ([], [])            
            print(f"Selected motion files: {self.files_path}")

        self.amp_loader = AMPLoader(motion_files=self.files_path, device=device, time_between_frames=time_between_frames)

    def get_motion_path(self,cfg):
        files_path = []; files_names = []
        path_to_files = os.path.join(self.legged_gym_root_dir, cfg.env.amp_motion_files[0])
        for f in os.listdir(path_to_files):
            files_path.append(os.path.join(path_to_files,f))
            files_names.append(f.split('.')[0])
        return files_path, files_names

    def get_full_frame_batch(self, batch_size):
        """ Returns a full batch of frames for the given batch size """
        return self.amp_loader.get_full_frame_batch(batch_size)
    
    def get_joint_pose_batch(self, batch):
        """ Returns a batch of joint poses for the given batch size """
        return self.amp_loader.get_joint_pose_batch(batch)
    
    def get_joint_vel_batch(self, batch):
        """ Returns a batch of joint velocities for the given batch size """
        return self.amp_loader.get_joint_vel_batch(batch)
    def get_root_pos_batch(self, batch):
        """ Returns a batch of root positions for the given batch size """
        return self.amp_loader.get_root_pos_batch(batch)
    def get_root_rot_batch(self, batch):
        """ Returns a batch of root rotations for the given batch size """
        return self.amp_loader.get_root_rot_batch(batch)
    def get_linear_vel_batch(self, batch):
        """ Returns a batch of linear velocities for the given batch size """
        return self.amp_loader.get_linear_vel_batch(batch)
    def get_angular_vel_batch(self, batch):
        """ Returns a batch of angular velocities for the given batch size """
        return self.amp_loader.get_angular_vel_batch(batch)