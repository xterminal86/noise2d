import math;
import random;

from noise1d import Noise1D;
from enum    import Enum, auto;
from utils   import Dot, Interpolate, Interpolation, VectorFromAngle;

################################################################################

class GradientMode(Enum):
  GRAD_RND = auto();
  GRAD_45  = auto();

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

class Noise2D:
  _gradients  = [];
  _resolution = 16;
  _step       = 1
  _maxVecLen  = 0.0;

  _gradientsOffsetsTable = [];
  
  _noise1dRef : Noise1D = None;
  
  _animationStep = 0.1;

  _gradientMode = GradientMode.GRAD_RND;

  # ----------------------------------------------------------------------------

  def __init__(self, resolution : int, step : int, gradientMode : GradientMode = GradientMode.GRAD_RND):
    self._resolution   = resolution;
    self._step         = step;
    self._gradientMode = gradientMode;

    self._maxVecLen = math.sqrt(step * step);

    self._gradients    = [ [ 0 for _ in range(resolution) ] for _ in range(resolution) ];
    self._gradientsOffsetsTable = [ [ 0 for _ in range(resolution) ] for _ in range(resolution) ];
    
    cnt = 0;
    
    for x in range(resolution):
      for y in range(resolution):
        self._gradients[x][y] = (
          GetRandomGradient() if self._gradientMode == GradientMode.GRAD_RND else GetRandomGradient45()
        );

        self._gradientsOffsetsTable[x][y] = random.randint(0, 359);

  # ----------------------------------------------------------------------------
  
  def GetGradientFromNoise(self, animator : float) -> tuple:
    noiseVal = self._noise1dRef.Noise(animator,
                                      self._noise1dRef._interpolationMode);
    
    cx = math.cos(noiseVal);
    cy = math.sin(noiseVal);
    
    return (cx, cy);
  
  # ----------------------------------------------------------------------------
  
  def Drive(self, animator : float, fromNoise : bool) -> float:
    newAnimatorValue = animator;
    
    for x in range(self._resolution):
      for y in range(self._resolution):
        offsetHere = self._gradientsOffsetsTable[x][y];
        if fromNoise:
          self._gradients[x][y] = self.GetGradientFromNoise(newAnimatorValue + offsetHere);
          newAnimatorValue += 0.0005;
        else:
          self._gradients[x][y] = VectorFromAngle(newAnimatorValue + offsetHere);
          newAnimatorValue += self._animationStep;
    
    return newAnimatorValue;

  # ----------------------------------------------------------------------------

  def Noise(self, x : int, y : int) -> float:
    cellX = x // self._step;
    cellY = y // self._step;

    offsetX = (x % self._step);
    offsetY = (y % self._step);

    #
    # step = 10
    #
    # (0;0)       (10;0)
    #   x--3------x
    #   |  .      .
    #   |  .      .
    #   |  .      .
    #   4..P      .
    #   |         .
    #   |         .
    #   |         .
    #   |         .
    #   |         .
    #   x.........x
    # (0;10)      (10;10)
    #
    # UL = ( 0; 0)
    # UR = (10; 0)
    # DL = ( 0;10)
    # DR = (10;10)
    #
    # P = (3;4)
    #
    # V1 = P
    # UR + V2 = V1 -> V2 = V1 - UR
    # DL + V3 = V1 -> V3 = V1 - DL
    # DR + V4 = V1 -> V4 = V1 - DR
    #

    V1 = (offsetX,              offsetY);
    V2 = (offsetX - self._step, offsetY);
    V3 = (offsetX,              offsetY - self._step);
    V4 = (offsetX - self._step, offsetY - self._step);

    #print(f"{ x }, { y } -> ({ cellY }, { cellX }) : ({ offsetX }, { offsetY })");

    ul = (cellY % self._resolution, cellX % self._resolution);
    ur = (cellY % self._resolution, (cellX + 1) % self._resolution);
    dl = ((cellY + 1) % self._resolution, cellX % self._resolution);
    dr = ((cellY + 1) % self._resolution, (cellX + 1) % self._resolution);

    #print(f"{ ul } - { ur }");
    #print(f"|        |");
    #print(f"{ dl } - { dr }");

    gul = self._gradients[ ul[0] ][ ul[1] ];
    gur = self._gradients[ ur[0] ][ ur[1] ];
    gdl = self._gradients[ dl[0] ][ dl[1] ];
    gdr = self._gradients[ dr[0] ][ dr[1] ];

    #print(f"grad ul - { gul }");
    #print(f"grad ur - { gur }");
    #print(f"grad dl - { gdl }");
    #print(f"grad dr - { gdr }");

    dotV1 = Dot(V1, gul);
    dotV2 = Dot(V2, gur);
    dotV3 = Dot(V3, gdl);
    dotV4 = Dot(V4, gdr);

    # print("-"*80);
    # print(f"{dotV1:8.2f} - {dotV2:8.2f}");
    # print(f"    |          |");
    # print(f"{dotV3:8.2f} - {dotV4:8.2f}");
    # print("-"*80);

    #res = (dotV1 + dotV2 + dotV3 + dotV4) / 4.0;
   
    r1 = Interpolate(dotV1, dotV2, (offsetX / self._step), Interpolation.COSINE);
    r2 = Interpolate(dotV3, dotV4, (offsetX / self._step), Interpolation.COSINE);

    res = Interpolate(r1, r2, (offsetY / self._step), Interpolation.COSINE);
    
    return res;

################################################################################
