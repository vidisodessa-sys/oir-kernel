import argparse
import json
import sys
from pathlib import Path
import numpy as np

from .core import oir_correlator

PRESETS = {
    # CHSH (четыре направления в плоскости x–y)
    "chsh": [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [1/np.sqrt(2), 1/np.sqrt(2), 0.0],
        [1/np.sqrt(2), -1/np.sqrt(2), 0.0],
    ],
    # GHZ три анализатора 120° на окружности (пример)
    "ghz": [
        [1.0, 0.0, 0.0],
        [-0.5, np.sqrt(3)/2, 0.0],
        [-0.5, -np.sqrt(3)/2, 0.0],
    ],
}

def load_axes(path: Path):
    """
    Загружает векторы-анализаторы из файла:
    - CSV: три столбца x,y,z без заголовка
    - JSON: список списков [[x,y,z], ...]
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)

    if p.suffix.lower() == ".csv":
        data = []
        for line in p.read_text().strip().splitlines():
            parts = [float(t) for t in line.replace(";", ",").split(",")[:3]]
            data.append(parts)
        return data
    elif p.suffix.lower() == ".json":
        return json.loads(p.read_text())
    else:
        raise ValueError("Unsupported file format (use .csv or .json)")

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="oir",
        description="OIR CLI — вычисление корреляторов Orientation Integral Rule",
    )
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--preset", choices=sorted(PRESETS.keys()),
                   help="готовый набор направлений (chsh, ghz)")
    g.add_argument("--axes-file", type=str,
                   help="путь к CSV/JSON с векторами (по одному в строке)")

    parser.add_argument("--eps", type=float, default=0.0,
                        help="анизотропия ε (по умолчанию 0.0)")
    parser.add_argument("-M", type=int, default=100000,
                        help="число сэмплов Монте-Карло (по умолчанию 100000)")
    args = parser.parse_args(argv)

    if args.preset:
        axes = PRESETS[args.preset]
    else:
        axes = load_axes(Path(args.axes_file))

    axes_np = [np.array(v, dtype=float) for v in axes]
    val = oir_correlator(axes_np, eps=args.eps, M=args.M)
    print(f"axes={len(axes_np)}, eps={args.eps}, M={args.M}")
    print(f"OIR correlator: {val:.12f}")

if __name__ == "__main__":
    main()
