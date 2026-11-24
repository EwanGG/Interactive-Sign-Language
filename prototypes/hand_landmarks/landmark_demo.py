"""Signova first data-processing prototype. Authoring support: ChatGPT.

Run: python landmark_demo.py
Optional real exported input: python landmark_demo.py hand.json
JSON format: {"coordinate_system": "image_normalised_xy",
 "image_width": 640, "image_height": 480,
 "landmarks": [[x, y], ...]}
Points must be consistently ordered. Index 0 is the wrist; index 9 is the
chosen scale reference. Confirm these indices with the detection teammate.
No camera access, recording, network access or third-party packages.
The default examples are synthetic geometry, not validated language signs.
"""

import json
import math
import sys


def validate_points(points):
    if len(points) != 21:
        raise ValueError("Expected 21 ordered points; confirm the detector format.")
    for point in points:
        if len(point) != 2 or any(
            isinstance(v, bool) or not isinstance(v, (int, float))
            or not math.isfinite(v) for v in point
        ):
            raise ValueError("Each point must contain two finite numbers.")


def normalise(points):
    """Accept consistent 2D pixel coordinates, centre on wrist, scale by 0-to-9."""
    validate_points(points)
    wx, wy = points[0]
    scale = math.dist(points[0], points[9])
    if scale < 1e-9:
        raise ValueError("Wrist and scale reference overlap; reject this frame.")
    return [((x - wx) / scale, (y - wy) / scale) for x, y in points]


def mean_distance(first, second):
    """Mean landmark distance in hand-scale units; not an accuracy percentage."""
    return sum(math.dist(a, b) for a, b in zip(first, second)) / len(first)


def load_export(path):
    with open(path, encoding="utf-8") as source:
        record = json.load(source)
    if record.get("coordinate_system") != "image_normalised_xy":
        raise ValueError("Input must explicitly use image_normalised_xy.")
    width, height = record["image_width"], record["image_height"]
    if any(isinstance(v, bool) or not isinstance(v, (int, float))
           or not math.isfinite(v) or v <= 0 for v in (width, height)):
        raise ValueError("Image dimensions must be finite positive numbers.")
    points = record["landmarks"]
    validate_points(points)
    # x and y use different image dimensions: convert both to pixels first.
    return [(x * width, y * height) for x, y in points]


def main():
    if len(sys.argv) == 2:
        result = normalise(load_export(sys.argv[1]))
        print("Normalised coordinates (wrist-centred, hand-scale units):")
        print(json.dumps(result, indent=2))
        return

    # Illustrative layout only: 1 wrist and 4 points for each of 5 fingers.
    reference = [(100.0, 200.0)]
    for finger in range(5):
        for joint in range(4):
            reference.append((60.0 + 20 * finger, 180.0 - 20 * joint))

    moved = [(x + 80, y + 35) for x, y in reference]
    resized = [(1.7 * x + 20, 1.7 * y - 15) for x, y in reference]
    changed = list(reference)
    changed[8] = (changed[8][0] + 20, changed[8][1] + 30)

    baseline = normalise(reference)
    print("SYNTHETIC DATA DEMO - not sign recognition results")
    print("Example                           Raw distance   Normalised distance")
    for name, points in [("Same geometry, moved", moved),
                         ("Same geometry, resized", resized),
                         ("One landmark changed", changed)]:
        distance = mean_distance(baseline, normalise(points))
        print(f"{name:33} {mean_distance(reference, points):12.6f} {distance:21.6f}")

    assert mean_distance(baseline, normalise(moved)) < 1e-9
    assert mean_distance(baseline, normalise(resized)) < 1e-9
    assert mean_distance(baseline, normalise(changed)) > 0
    try:
        normalise([(0, 0)] * 21)
    except ValueError:
        pass
    else:
        raise AssertionError("Degenerate geometry must be rejected")
    print("PASS: translation, uniform scaling, changed geometry and invalid scale checks")
    print("Limits: no rotation/perspective correction; no sign labels or teaching scores.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"Input error: {error}", file=sys.stderr)
        sys.exit(1)
