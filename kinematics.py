"""Kinematics of the Gen3 Lite for my midterm.

The grader reads the values below without running this file, so write numbers
directly. You may use pi, + - * /, and np.array([...]). Lengths are in meters
and angles in radians. Replace every None.
"""
from math import pi

# "classical" (standard) or "modified" (Craig) DH.
CONVENTION = "classical"

# One row per joint, joint 1 first. theta_i = q_i + theta_offset, where q_i is the
# joint value reported in /joint_states. Frame 0 is base_link. The last frame has
# its origin at end_effector_link and its z axis along the marker.
DH = [
    {"alpha": None, "a": None, "d": None, "theta_offset": None},  # joint 1
    {"alpha": None, "a": None, "d": None, "theta_offset": None},  # joint 2
    {"alpha": None, "a": None, "d": None, "theta_offset": None},  # joint 3
    {"alpha": None, "a": None, "d": None, "theta_offset": None},  # joint 4
    {"alpha": None, "a": None, "d": None, "theta_offset": None},  # joint 5
    {"alpha": None, "a": None, "d": None, "theta_offset": None},  # joint 6
]

# Your three key poses: joint values q1 to q6 in radians, as in /joint_states.
# Rename the keys to describe each pose.
KEY_POSES = {
    "key_pose_1": [None, None, None, None, None, None],
    "key_pose_2": [None, None, None, None, None, None],
    "key_pose_3": [None, None, None, None, None, None],
}

# The Jacobian at one of your key poses, in base_link, for the origin of
# end_effector_link. Rows: vx, vy, vz, wx, wy, wz. Columns: joints 1 to 6.
JACOBIAN_POSE = "key_pose_1"
JACOBIAN = [
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
]
