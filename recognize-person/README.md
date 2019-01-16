# Recognize a Person

To run this sample program, you need Python3.6 or later.

You also need to make a couple of changes to reco.py:

1. near the beginning, change self.engine_ip to your IP address (where CamviServer is running).
2. near the end, change the open image call to an actual file path on your system.

After making the change, simply run this in the command console:

> python3 reco.py

Sample output:
```
{'confidence': 0.75, 'name': 'Garner', 'person': 6829, 'face': 7318}
```

