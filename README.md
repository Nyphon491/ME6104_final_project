# Problem Statement 

One of the main benefits of additive manufacturing (AM) processes is the rapid production of prototypes. AM is defined by the ASTM society as “a process of joining materials to make objects from 3D model data, usually layer upon layer, as opposed to subtractive manufacturing methodologies”. Fused Deposition Modeling (FDM) is an AM 3D printing technology that builds objects layer by layer by extruding thermoplastic filament through a heated nozzle. A unique benefit of FDM is control over the interior of solids via an infill pattern. There is significant interest in infill patterns that offer isotropic mechanical properties agnostic to part geometry balanced relative to infill density and production speed. 

# Approach 

Conventionally AM machines work by cartesian coordinate movements with each axis of movement controlled by a single motor. This configuration requires diagonal movements to be completed by the two motors in unison. As a result, infill patterns created largely from diagonal movements will increase production speed. We aim to create a tool that improves production time by discretizing common infill patterns to be increasingly composed of diagonal lines. This tool will take a parametric representation of an infill pattern unit cell layer-wise, sample a set of points along the curves, and then create increasingly more diagonal line segments from an ordered set of candidate point pairs. This set will be ordered by difference of the angle of the associated line segment to ±45° with respect to the coordinate axes along which the print head moves. It will then export the new “diagonalized” infill pattern as a Gcode file. 

# To do

* [ ] make slice-wise curves a single composite curve
  * [ ] both bezier and line segments
  * [ ] extract shifted locations from original points
* [ ] measure error of new slice to old slice
* [ ] sweep over `n` and `a` to find *acceptable* (diminishing returns) new slice