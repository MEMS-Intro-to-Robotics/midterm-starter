# Midterm Project: Whiteboard Writing: [Your Name]

ECE 383 / ME 555: Introduction to Robotics and Automation (Fall 2026)

Update this README with your name, NetID, and a 1–3 line summary of your work.

## Contents

- `test_midterm.py`: automated repository checks
- `pytest.ini`: limits `pytest` to `test_midterm.py` so it skips the ROS 2
  workspace

Create your ROS 2 package under `ros2_ws/src/`, as in Lab 6. The midterm
handout gives the whiteboard station values, the writing box, and the task.

## Run the grading checks

From the repository root on the VM:

```bash
pytest -v
```

The checks look for an updated README and a ROS 2 package under
`ros2_ws/src/` with Python code that parses and defines at least one function.
Tracked ROS 2 build output produces a warning.

Course staff grade your writeup and code from the Gradescope PDF and your
whiteboard run at the lab station.

Before your final push, run the checks and fix any failures. Then confirm that
Classroom 50 reports a passing result.
