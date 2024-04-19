import math;
import random;

################################################################################

def GetRandomGradient() -> tuple:
  rndX = (-1 if random.randint(0, 1) == 1 else 1) * random.random();
  rndY = (-1 if random.randint(0, 1) == 1 else 1) * random.random();

  ln = math.sqrt(pow(rndX, 2) + pow(rndY, 2));

  return (rndX / ln, rndY / ln);

################################################################################

def GetRandomGradient45() -> tuple:
  grads = [
    ( 0.7071067811865475,  0.7071067811865475),
    (-0.7071067811865475,  0.7071067811865475),
    (-0.7071067811865475, -0.7071067811865475),
    ( 0.7071067811865475, -0.7071067811865475)
  ];

  return random.choice(grads);

################################################################################

class NewNoise2D:
  _gradients  = [];
  _resolution = 16;
  _step       = 1

  # ----------------------------------------------------------------------------

  def __init__(self, resolution, step):
    self._resolution = resolution;
    self._step       = step;

    self._gradients = [ [ 0 for _ in range(resolution) ] for _ in range(resolution) ];

    for x in range(resolution):
      for y in range(resolution):
        self._gradients[x][y] = GetRandomGradient();
        #self._gradients[x][y] = GetRandomGradient45();
        #print((
        #  f"({x:2d}, {y:2d}) -> ({self._gradients[x][y][0]:.4f}, "
        #  f"{self._gradients[x][y][1]:.4f})"
        #));

  # ----------------------------------------------------------------------------

  def Noise(self, x : int, y : int) -> float:
    cellX = x // self._step;
    cellY = y // self._step;

    offsetX = (x % self._step);
    offsetY = (y % self._step);

    print(f"{ x }, { y } -> ({ cellY }, { cellX }) : ({ offsetX }, { offsetY })");

    ul = (cellY,     cellX);
    ur = (cellY,     cellX + 1);
    dl = (cellY + 1, cellX);
    dr = (cellY + 1, cellX + 1);

    print(f"{ ul } - { ur }");
    print("|             |");
    print(f"{ dl } - { dr }");

    gul = self._gradients[ ul[0] ][ ul[1] ];
    gur = self._gradients[ ur[0] ][ ur[1] ];
    gdl = self._gradients[ dl[0] ][ dl[1] ];
    gdr = self._gradients[ dr[0] ][ dr[1] ];

    print(f"grad ul - { gul }");
    print(f"grad ur - { gur }");
    print(f"grad dl - { gdl }");
    print(f"grad dr - { gdr }");

    return 1.0;

################################################################################
