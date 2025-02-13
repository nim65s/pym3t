"""
Example with full options:
python run_realsense_example.py --use_region --use_depth --use_texture --measure_occlusions --use_depth_viewer -b obj_000014 -m <path/to/obj/dir>
"""

import argparse

import numpy as np
import quaternion
from single_view_tracker_example import setup_single_object_tracker

import pym3t


def parse_script_input():
    parser = argparse.ArgumentParser(
        prog="run_realsense_example",
        description="Run the m3t tracker using realsense camera video stream",
    )

    parser.add_argument(
        "-b",
        "--body_name",
        dest="body_name",
        type=str,
        required=True,
        help="Name of the object to track. need to match",
    )
    parser.add_argument(
        "-m",
        "--models_dir",
        dest="models_dir",
        type=str,
        required=True,
        help="Path to directory where object model file {body_name}.obj is stored",
    )
    parser.add_argument(
        "--scale_geometry",
        dest="scale_geometry",
        default=0.001,
        type=float,
        required=False,
        help="Scale factor to convert model geometry to meters.",
    )
    parser.add_argument(
        "--tmp_dir",
        dest="tmp_dir",
        type=str,
        default="tmp",
        help="Directory to store preprocessing files generated by the tracker.",
    )
    parser.add_argument(
        "--use_region", dest="use_region", action="store_true", default=False
    )
    parser.add_argument(
        "--use_depth", dest="use_depth", action="store_true", default=False
    )
    parser.add_argument(
        "--use_texture", dest="use_texture", action="store_true", default=False
    )
    parser.add_argument(
        "--use_depth_viewer",
        dest="use_depth_viewer",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--model_occlusions",
        dest="model_occlusions",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--measure_occlusions",
        dest="measure_occlusions",
        action="store_true",
        default=False,
    )

    return parser.parse_args()


args = parse_script_input()

# Setup tracker and all related objects
if args.use_depth:
    (
        tracker,
        optimizer,
        body,
        link,
        color_camera,
        depth_camera,
        color_viewer,
        depth_viewer,
    ) = setup_single_object_tracker(args, use_realsense=True)
else:
    (
        tracker,
        optimizer,
        body,
        link,
        color_camera,
        color_viewer,
    ) = setup_single_object_tracker(args, use_realsense=True)

# ----------------
# Initialize object pose
body2world_pose = np.array(
    [1, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0.556, 0, 0, 0, 1]
).reshape((4, 4))
dR_l = quaternion.as_rotation_matrix(quaternion.from_rotation_vector([0.2, 0, 0.0]))
body2world_pose[:3, :3] = body2world_pose[:3, :3] @ dR_l
# ----------------

detector = pym3t.StaticDetector("static_detector", optimizer, body2world_pose, False)
tracker.AddDetector(detector)

ok = tracker.SetUp()
print("tracker.SetUp ok: ", ok)
names_detecting = {args.body_name}
names_starting = {args.body_name}
tracker.RunTrackerProcess(
    execute_detection=True,
    start_tracking=True,
    names_detecting=names_detecting,
    names_starting=names_starting,
)
