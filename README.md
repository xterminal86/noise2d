```
usage: main.py [-h] [--seed SEED] [--debug]
               [--scale {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40}]
               RESOLUTION

Use 1 or 2 to change between static and animatied modes. 
Use '+' or '-' to change animation speed. 
Use 'C' to change color scheme. 
Use 'G' to toggle gradients type (static mode only). 
Press 'H' to toggle debug gizmos. 
Press 'F' to toggle between fast and precise draw. 
Press 'N' to toggle between circular / noise gradient vectors. 
Press 'I' to toggle noise interpolation mode (noise gradients only).
Press LMB to check noise value under cursor point. 
'Escape' to quit.

positional arguments:
  RESOLUTION            Noise grid resolution. E.g. 32

options:
  -h, --help            show this help message and exit
  --seed SEED           RNG seed. E.g. 1234. Default: None
  --debug               Show debug gizmos. Default: off
  --scale {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40}
                        Screen size scale factor. Default: 10
```

![](animation.gif)
![](noise-gradients.gif)
