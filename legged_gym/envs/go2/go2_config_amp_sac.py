
from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg

# folder relative to LEGGED_GYM_ROOT_DIR, every file inside is loaded
MOTION_FILES = ["datasets/mocap_motions_go2"]


class GO2AMPSACCfg( LeggedRobotCfg ):

    class env( LeggedRobotCfg.env ):

        num_observations = 40 # 
        num_privileged_obs = 46 #
        include_history_steps = None          
        
        amp_loader = True # 
        amp_motion_files = MOTION_FILES
        selected_motion_names = []
        reference_state_initialization = True 

        episode_length_s = 20 
        ee_names = ["FL_foot", "FR_foot", "RL_foot", "RR_foot"]
        
        #command velocity  - Joystick control 
        get_commands_directions_sampled = True
        get_commands_from_joystick = False

    class terrain( LeggedRobotCfg.terrain ):
        mesh_type = "plane" #'rough' #'trimesh' #'plane'
        measure_heights = False
        curriculum = False#

        # terrain scaling
        horizontal_scale = 0.1 # [m]
        vertical_scale = 0.005 # [m]

        border_size = 25 # [m]
        static_friction = 1.0
        dynamic_friction = 1.0
        restitution = 0.


    class commands:
        curriculum = False
        max_curriculum = 1.
        num_commands = 4 # default: lin_vel_x, lin_vel_y, ang_vel_yaw, heading (in heading mode ang_vel_yaw is recomputed from heading error)
        resampling_time = 10. # time before command are changed[s]
        heading_command = False # if true: compute ang vel command from heading error: for smoother turning behavior in multi-gait training 
        class ranges:
            lin_vel_x = [0.65, 1.5] #[-2.0, 2.0] # min max [m/s]
            lin_vel_y = [-0., 0.]#[-0.3, 0.3]   # min max [m/s]
            ang_vel_yaw = [-0., 0.] #[-1.57, 1.57]    # min max [rad/s]
            heading = [-3.14, 3.14]

    class init_state( LeggedRobotCfg.init_state ):
        pos = [0.0, 0.0, 0.42] # x,y,z [m]
        default_joint_angles = {
            'FL_hip_joint': 0.1,   
            'RL_hip_joint': 0.1,   
            'FR_hip_joint': -0.1 ,  
            'RR_hip_joint': -0.1,   

            'FL_thigh_joint': 0.8,     
            'RL_thigh_joint': 1.,   
            'FR_thigh_joint': 0.8,     
            'RR_thigh_joint': 1.,   

            'FL_calf_joint': -1.5,   
            'RL_calf_joint': -1.5,    
            'FR_calf_joint': -1.5,  
            'RR_calf_joint': -1.5,    
        }
    class control( LeggedRobotCfg.control ):
        # PD Drive parameters:
        control_type = 'P'
        stiffness = {'joint': 20.}  # [N*m/rad]
        damping = {'joint': 0.5}     # [N*m*s/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.25
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 6
    
    class asset( LeggedRobotCfg.asset ):
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/go2/urdf/go2_limited.urdf'
        foot_name = "foot"
        penalize_contacts_on = ["thigh", "calf"]
        terminate_after_contacts_on = [
            "base", "FL_calf", "FR_calf", "RL_calf", "RR_calf",
            "FL_thigh", "FR_thigh", "RL_thigh", "RR_thigh"]
        self_collisions = 0 # 1 to disable, 0 to enable...bitwise filter

        disable_gravity = False
        collapse_fixed_joints = True # merge bodies connected by fixed joints. Specific fixed joints can be kept by adding " <... dont_collapse="true">
        fix_base_link = False # fixe the base of the robot
        default_dof_drive_mode = 3 # see GymDofDriveModeFlags (0 is none, 1 is pos tgt, 2 is vel tgt, 3 effort)
        replace_cylinder_with_capsule = True # replace collision cylinders with capsules, leads to faster/more stable simulation
        flip_visual_attachments = True # Some .obj meshes must be flipped from y-up to z-up
        
        density = 0.001
        angular_damping = 0.
        linear_damping = 0.
        max_angular_velocity = 1000.
        max_linear_velocity = 1000.
        armature = 0.
        thickness = 0.01

    class domain_rand:
        randomize_friction = True
        friction_range = [0.25, 1.75] #[0.25, 2.5] - complex terrain
        randomize_base_mass = True
        added_mass_range = [-1., 1.]
        push_robots = False
        push_interval_s = 15
        max_push_vel_xy = 0.25
        randomize_gains = True
        stiffness_multiplier_range = [0.9, 1.1]
        damping_multiplier_range = [0.9, 1.1]

    class rewards( LeggedRobotCfg.rewards ):
        soft_dof_pos_limit = 1. #0.9
        soft_dof_vel_limit = 1.
        soft_torque_limit = 1. #0.6

        base_height_target = 0.32 #0.32 unenven terrain

        only_positive_rewards = True # if true negative total rewards are clipped at zero (avoids early termination problems)
        tracking_sigma = 0.25 # tracking reward = exp(-error^2/sigma)

        max_contact_force = 100. # forces above this value are penalized
        min_distance_foot_ground = 0.05 # 5cm


        class scales( LeggedRobotCfg.rewards.scales ):
            
            tracking_lin_vel = 0.

            tracking_lin_vel_x = 2.5 
            tracking_lin_vel_y = 0. #0.05

            tracking_ang_vel = 0. #0.5 #* 1. / (.005 * 6) -- YAW

            torques = -0.00005 # Penalize torques
            dof_acc = -2.5e-7 #  Penalize dof accelerations
            dof_vel = 0. #-0.05 # Penalize dof velocities
            
            action_rate = 0. #-0.01 ## Penalize changes in actions

            termination = 0. #-0.5 #Penalizer termination

            lin_vel_z = -15.  # Penalize z axis base linear velocity #decrease
            ang_vel_xy = -1.  # Penalize xy axes base angular velocity #
            ang_vel_z = -5. # Penalize z axes (Yaw) base angular velocity

            orientation = 0 #Penalize non flat base orientation

            torque_limits = 0. #-0.002  #-0.0002 # Penalize torques too close to the limit
            dof_pos_limits = -4 #-2. #-2. #-4.0 #-2 ## Penalize dof positions too close to the limit
            dof_vel_limits = 0. #-0.1 #-0.05 #-0.05 # Penalize dof velocities too close to the limit

            collision = -1. #Penalize collision

            base_height = -2 #-0.05 #Penalize base height away from target
            
            feet_contact_forces = -2
            feet_air_time = 1. #0.5 #0.05 #1.0 # Reward long steps                        
            
            feet_stumble = 0.0 # Penalize feet hitting vertical surfaces
            
            swing_clearance = 0. #4.

            stand_still = -0. #-0.5 #-0.05 #Penalize motion if standing still and should be moving            
            #speed_deviation = -0.05 #Penalize deviation
            

    class normalization:
        class obs_scales:
            lin_vel = 2.0
            ang_vel = 0.25
            dof_pos = 1.0
            dof_vel = 0.05
            height_measurements = 5.0
        clip_observations = 100.
        clip_actions = 100.


    class noise:
        add_noise = True
        noise_level = 1.0 # scales other values
        class noise_scales:
            dof_pos = 0.03
            dof_vel = 1.5
            lin_vel = 0.1
            ang_vel = 0.3
            gravity = 0.05
            height_measurements = 0.1

    # viewer camera:
    class viewer:
        ref_env = 0
        pos = [10, 0, 6]  # [m]
        lookat = [11., 5, 3.]  # [m]


    class sim:
        dt =  0.005 #->5ms (200Hz)
        substeps = 2 # number of substeps per sim step = 0.0025 (2.5ms) -  effective physics rate  400Hz
        gravity = [0., 0. ,-9.81]  # [m/s^2]
        up_axis = 1  # 0 is y, 1 is z

        class physx:
            num_threads = 10
            solver_type = 1  # 0: pgs, 1: tgs
            num_position_iterations = 4 # penetration, joint error correction, contact stability
            num_velocity_iterations = 1 # default is 1 friction, restitution, damping, torque limits
            contact_offset = 0.01  # [m]
            rest_offset = 0.0   # [m]
            bounce_threshold_velocity = 0.5 #0.5 [m/s]
            max_depenetration_velocity = 1.0
            max_gpu_contact_pairs = 2**23 #2**24 -> needed for 8000 envs and more
            default_buffer_size_multiplier = 5
            contact_collection = 2 # 0: never, 1: last sub-step, 2: all sub-steps (default=2)


