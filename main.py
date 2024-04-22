import argparse;
import random;
import sys;

import pygame;

# from noise2d import Noise2D, Interpolation;
from noise2d_new import NewNoise2D;
from utils       import NoiseToColor;

################################################################################

class ProgramData:
  _shouldStop = False;
  _seed       = 1;
  _resolution = 16;
  _step       = 1;
  _screenSize = tuple();
  _noiseObj   = None;
  _drawData   = [];
  _noiseData  = [];
  _debugMode  = True;
  _maxNoise   = -sys.maxsize;
  _minNoise   = sys.maxsize;

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
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        noiseVal = pd._noiseObj.Noise(event.pos[0], event.pos[1]);
        print(f"Noise here: {noiseVal:.2f}");

################################################################################

def Draw(screen, pd : ProgramData):
  screen.fill( (0, 0, 0) );

  for x in range(pd._screenSize[0]):
    for y in range(pd._screenSize[1]):
      pygame.draw.circle(screen, pd._drawData[x][y], (x, y), 1);

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

def main():
  screenSizeMin = ( 80, 60 );
  maxScaleChoices = [];

  for i in range(40):
    maxScaleChoices.append(i + 1);

  parser = argparse.ArgumentParser();

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

  scale = args.scale;

  pygame.init();

  pygame.display.set_caption("noise2d demo");

  screenSize = ( screenSizeMin[0] * scale, screenSizeMin[1] * scale );

  screen = pygame.display.set_mode(screenSize);

  pd = ProgramData();
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

  clock = pygame.time.Clock();

  pd._noiseObj = NewNoise2D(pd._resolution, pd._step);

  pd._drawData  = [ [ 0.0 for _ in range(screenSize[1]) ] for _ in range(screenSize[0]) ];
  pd._noiseData = [ [ 0.0 for _ in range(screenSize[1]) ] for _ in range(screenSize[0]) ];

  for x in range(screenSize[0]):
    for y in range(screenSize[1]):
      noiseVal = pd._noiseObj.Noise(x, y);

      if (noiseVal > pd._maxNoise):
        pd._maxNoise = noiseVal;

      if (noiseVal < pd._minNoise):
        pd._minNoise = noiseVal;

      pd._noiseData[x][y] = noiseVal;

  for x in range(screenSize[0]):
    for y in range(screenSize[1]):
      coeff = pd._noiseData[x][y] / pd._maxNoise;
      clr = coeff * 255.0;
      pd._drawData[x][y] = NoiseToColor(clr);

  print("Noise generation done");
  print(f"Max noise: { pd._maxNoise }");
  print(f"Min noise: { pd._minNoise }");

  while not pd._shouldStop:

    clock.tick(60);

    ProcessEvents(pd);
    Draw(screen, pd);

  pygame.quit();

  '''
  bias = 1.0;
  intpl = Interpolation.LINEAR;
  noise = Noise2D(size, seed=seed, interpolation=intpl, scalingBias=bias);

  while running:

    clock.tick(60);

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False;
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          running = False;
        elif event.key == pygame.K_i:
          if intpl == Interpolation.LINEAR:
            intpl = Interpolation.COSINE;
          else:
            intpl = Interpolation.LINEAR;

          print(intpl);

          noise = Noise2D(size, seed=seed, interpolation=intpl, scalingBias=bias);
        elif event.key == pygame.K_z:
          bias -= 0.1;

          if bias < 0.1:
            bias = 0.1;

          print(f"bias = { bias }");

          noise = Noise2D(size, seed=seed, interpolation=intpl, scalingBias=bias);

        elif event.key == pygame.K_x:
          bias += 0.1;

          if bias > 2.0:
            bias = 2.0;

          print(f"bias = { bias }");

          noise = Noise2D(size, seed=seed, interpolation=intpl, scalingBias=bias);

    screen.fill((0,0,0));

    for x in range(screenSize[0]):
      for y in range(screenSize[1]):
        c = int(noise.Noise(x, y) * 255);
        if c > 255:
          c = 255;

        clr = (c, c, c);

        pygame.draw.circle(screen,
                           clr,
                           (x, y),
                           1);

    pygame.display.flip();

  pygame.quit();
  '''

################################################################################

if __name__ == "__main__":
  main();
