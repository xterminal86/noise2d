import argparse;
import random;
import sys;

import pygame;

from enum    import Enum, auto;
from noise1d import Noise1D;
from noise2d import Noise2D, GradientMode;
from utils   import NoiseToColor, ColorSchemes, Interpolation;

class DisplayMode(Enum):
  ANIMATED = auto();
  STATIC   = auto();

################################################################################

class ProgramData:
  _noiseObj   : Noise2D = None;
  _noiseObj1d : Noise1D = None;
  
  _shouldStop        = False;
  _driveFromNoise    = False;
  
  _noise1dInterpolation = Interpolation.LINEAR;
  
  _seed           = 1;
  _resolution     = 16;
  _step           = 1;
  _screenSize     = tuple();
  _noiseData      = [];
  _debugMode      = True;
  _fastDraw       = True;
  _maxNoise       = -sys.maxsize;
  _minNoise       = sys.maxsize;
  _animator       = 0.0;
  _scale          = 1;
  _displayMode    = DisplayMode.ANIMATED;
  _gradientMode   = GradientMode.GRAD_RND;
  _colorSchemeInd = 0;

################################################################################

def ProcessEvents(pd : ProgramData):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pd._shouldStop = True;
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pd._shouldStop = True;
      elif event.key == pygame.K_h:
        pd._debugMode = not pd._debugMode;
      elif event.key == pygame.K_1:
        pd._displayMode = DisplayMode.STATIC;
        print("Display mode = STATIC");
      elif event.key == pygame.K_2:
        pd._displayMode = DisplayMode.ANIMATED;
        print("Display mode = ANIMATED");
      elif event.key == pygame.K_g:
        if pd._gradientMode == GradientMode.GRAD_RND:
          pd._gradientMode = GradientMode.GRAD_45;
          print("Gradient mode = GRAD_45");
        else:
          pd._gradientMode = GradientMode.GRAD_RND;
          print("Gradient mode = GRAD_RND");
      elif event.key == pygame.K_EQUALS:
        pd._noiseObj._animationStep += 0.1;
        print(f"Animation speed = {pd._noiseObj._animationStep:.2f}");
      elif event.key == pygame.K_MINUS:
        pd._noiseObj._animationStep += -0.1;
        if pd._noiseObj._animationStep < 0.1:
          pd._noiseObj._animationStep = 0.1;
        print(f"Animation speed = {pd._noiseObj._animationStep:.2f}");
      elif event.key == pygame.K_c:
        pd._colorSchemeInd += 1;
        pd._colorSchemeInd = (pd._colorSchemeInd % len(ColorSchemes));
        print(f"Selected color scheme: { ColorSchemes[pd._colorSchemeInd] }");
      elif (pd._displayMode == DisplayMode.STATIC) and (event.key == pygame.K_SPACE):
        PrepareNoiseData(pd);
        print("Recreated");
      elif event.key == pygame.K_f:
        pd._fastDraw = not pd._fastDraw;
        print(f"Fast draw = { pd._fastDraw }");
      elif event.key == pygame.K_n:
        pd._driveFromNoise = not pd._driveFromNoise;
        print(f"Drive from noise = { pd._driveFromNoise }");
      elif event.key == pygame.K_i:
        if pd._driveFromNoise:
          pd._noise1dInterpolation = Interpolation.LINEAR if pd._noise1dInterpolation == Interpolation.COSINE else Interpolation.COSINE;
          pd._noiseObj1d._interpolationMode = pd._noise1dInterpolation;
          print(f"Noise 1D interpolation mode = { pd._noise1dInterpolation }");
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        noiseVal = pd._noiseObj.Noise(event.pos[0], event.pos[1]);
        print(f"Noise here: {noiseVal:.2f}");

################################################################################

def DrawNoise(screen, pd : ProgramData):
  if pd._displayMode == DisplayMode.ANIMATED:
    pd._animator = pd._noiseObj.Drive(pd._animator, pd._driveFromNoise);

  for x in range(pd._screenSize[0]):
    for y in range(pd._screenSize[1]):
      coeff = pd._noiseObj.Noise(x, y) / pd._maxNoise;
      clr = coeff * 255.0;
      colorToDraw = NoiseToColor(clr, ColorSchemes[pd._colorSchemeInd]);
      pygame.draw.circle(screen, colorToDraw, (x, y), 1);

################################################################################

def DrawFast(screen, pd : ProgramData):
  nx = 0;
  ny = 0;

  step = pd._scale;
  
  if step > 8:
    step = step // 2;

  if pd._displayMode == DisplayMode.ANIMATED:
    pd._animator = pd._noiseObj.Drive(pd._animator, pd._driveFromNoise);

  for x in range(0, pd._screenSize[0], step):
    for y in range(0, pd._screenSize[1], step):
      coeff = pd._noiseObj.Noise(nx, ny) / pd._maxNoise;
      clr = coeff * 255.0;
      colorToDraw = NoiseToColor(clr, ColorSchemes[pd._colorSchemeInd]);
      pygame.draw.rect(screen, colorToDraw, pygame.Rect(x, y, step, step));
      ny += step;
    nx += step;
    ny = 0;

################################################################################

def Draw(screen, pd : ProgramData):
  screen.fill( (0, 0, 0) );

  if pd._fastDraw:
    DrawFast(screen, pd);
  else:
    DrawNoise(screen, pd);

  if pd._debugMode:
    gridColor    = pygame.Color("#AA00AA");
    gradVecColor = pygame.Color("#00AAAA");

    gradLen = pd._step // 2;

    for x in range(0, pd._screenSize[0], pd._step):
      pygame.draw.line(screen, gridColor, (x, 0), (x, pd._screenSize[1]));
      pygame.draw.line(screen, gridColor, (0, x), (pd._screenSize[0], x));

    for x in range(pd._resolution):
      for y in range(pd._resolution):
        gradVec = pd._noiseObj._gradients[x][y];
        gradVec = (gradVec[0] * gradLen, gradVec[1] * gradLen);

        cornerCoords = (y * pd._step, x * pd._step);
        vecEnd       = (cornerCoords[0] + gradVec[0], cornerCoords[1] + gradVec[1]);

        pygame.draw.line(screen, gradVecColor, cornerCoords, vecEnd);
        pygame.draw.circle(screen, gradVecColor, vecEnd, 2);

  pygame.display.flip();

################################################################################

def PrepareNoiseData(pd : ProgramData):
  pd._noiseObj = Noise2D(pd._resolution,
                         pd._step,
                         pd._gradientMode);
     
  pd._noiseObj1d = Noise1D(pd._resolution ** 2, 1.0, pd._seed);
  
  pd._noiseObj._noise1dRef = pd._noiseObj1d;
  
  for x in range(pd._screenSize[0]):
    for y in range(pd._screenSize[1]):
      noiseVal = pd._noiseObj.Noise(x, y);

      if (noiseVal > pd._maxNoise):
        pd._maxNoise = noiseVal;

      if (noiseVal < pd._minNoise):
        pd._minNoise = noiseVal;

      pd._noiseData[x][y] = noiseVal;

################################################################################

def main():
  screenSizeMin = ( 80, 60 );
  maxScaleChoices = [];

  for i in range(40):
    maxScaleChoices.append(i + 1);

  parser = argparse.ArgumentParser(description=(
    "Use 1 or 2 to change between static and animatied modes. "
    "Use '+' or '-' to change animation speed. "
    "Use 'C' to change color scheme. "
    "Use 'G' to toggle gradients type (static mode only). "
    "Press 'H' to toggle debug gizmos. "
    "Press 'F' to toggle between fast and precise draw. "
    "Press 'N' to toggle between circular / noise gradient vectors. "
    "Press 'I' to toggle noise interpolation mode (noise gradients only). "
    "Press LMB to check noise value under cursor point. "
    "'Escape' to quit. "
  ));

  parser.add_argument("RESOLUTION",
                      type=int,
                      help="Noise grid resolution. E.g. 32");
  parser.add_argument("--seed",
                      type=int,
                      default=None,
                      help="RNG seed. E.g. 1234. Default: None");
  parser.add_argument("--debug",
                      action="store_true",
                      help="Show debug gizmos. Default: off");
  parser.add_argument("--scale",
                      type=int,
                      choices=maxScaleChoices,
                      default=10,
                      help="Screen size scale factor. Default: 10");

  args = parser.parse_args();
  
  pygame.init();

  pygame.display.set_caption("noise2d demo");
  
  pd = ProgramData();
  
  pd._scale = args.scale;
  
  screenSize = ( screenSizeMin[0] * pd._scale, screenSizeMin[1] * pd._scale );

  screen = pygame.display.set_mode(screenSize);
  
  pd._resolution = args.RESOLUTION;
  pd._debugMode  = args.debug;

  if pd._resolution < 1:
    pd._resolution = 1;

  if pd._resolution > screenSize[1]:
    pd._resolution = screenSize[1];

  pd._seed       = args.seed;
  pd._screenSize = screenSize;
  pd._step       = pd._screenSize[0] // pd._resolution;

  print(f"STEP = { pd._step }");

  random.seed(pd._seed);

  pd._noiseData = [ [ 0.0 for _ in range(pd._screenSize[1]) ] for _ in range(pd._screenSize[0]) ];

  PrepareNoiseData(pd);

  clock = pygame.time.Clock();

  print("Noise generation done");
  print(f"Max noise: { pd._maxNoise }");
  print(f"Min noise: { pd._minNoise }");

  while not pd._shouldStop:

    clock.tick(60);

    ProcessEvents(pd);
    Draw(screen, pd);

  pygame.quit();

################################################################################

if __name__ == "__main__":
  main();
