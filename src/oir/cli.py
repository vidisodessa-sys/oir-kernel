import argparse
import numpy as np
from .core import oir_correlator

def parse_axes(name: str):
    """
    Примеры форматов:
      --axes "1,0,0; 0,1,0; 0.707,0.707,0; 0.707,-0.707,0"
      --axes-file axes.txt (по одному вектору в строке, через запятую)
    """
    vecs = []
    for part in name.split(";"):
        part = part.strip()
        if not part:
            continue
        x, y, z = map(float, part.split(","))
        v = np.array([x, y, z], dtype=float)
        v = v / np.linalg.norm(v)
        vecs.append(v)
    return vecs

def main():
    p = argparse.ArgumentParser(prog="oir", description="OIR kernel CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    chsh = sub.add_parser("chsh", help="Compute CHSH-like correlator from 4 axes")
    chsh.add_argument("--axes", type=str,
                      default="1,0,0; 0,1,0; 0.70710678,0.70710678,0; 0.70710678,-0.70710678,0",
                      help="4 unit vectors as 'x,y,z; ...'")
    chsh.add_argument("--eps", type=float, default=0.0, help="anisotropy ε")
    chsh.add_argument("--samples", type=int, default=100000, help="Monte Carlo samples M")

    args = p.parse_args()

    if args.cmd == "chsh":
        axes = parse_axes(args.axes)
        if len(axes) != 4:
            raise SystemExit("Need exactly 4 axes for CHSH")
        val = oir_correlator(axes, eps=args.eps, M=args.samples)
        print(f"CHSH correlator: {val:.9f}")

if __name__ == "__main__":
    main()
