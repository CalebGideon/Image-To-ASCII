# Image-To-ASCII: Using only Lower Level Memory Manipulation

<div>
  <h2>Table of Contents</h2>
</div>

<div>
  <ul>
    <li>Breakdown
    <ul>
      <li>Purpose</li>
      <li>Capabilities</li>
      <li>Limitations</li>
    </ul>
    </li>
    <li>How to Setup
    <ul>
      <li>Download</li>
      <li>Parameters & Examples</li>
      <li>Downsampling</li>
    </ul>
    </li>
    <li>Improvements Pending
    <ul>
      <li>More Efficient Downsampling</li>
      <li>32-bit BMP conversion function</li>
      <li>Specify I/O</li>
    </ul>
    </li>
  </ul>
</div>

<div>
  <h2>Breakdown</h2>
</div>

<div>
  <h3>Purpose</h3>
  <p>This repository aims to explore the process of Image to ASCII conversion without reliance on external Python libraries. The only dependencies for now include:</p>
  <ol>
    <li><b>import os to allow direct communication with file status using operating system, allows case checking for valid i/o paths</b></li>
    <li><b>import sys for reading command line arguments for user input verification</b></li>
    <li><b>import sys for reading command line arguments for user input verification</b></li>
    <li><b>PIL used only for converting all image types to BMP -> Will be phased out for custom conversion in different file formats</b></li>
  </ol>
</div>

<h3>Capabilities</h3>
  <p>This ASCII converter uses manipulation of image bit domain headers and data, to create specified functions allowing conversion across a multitude of file types and byte sizes:</p>
  <ol>
    <li><b>Supports all image types, e.g. PNG, BMP, JPG, JPEG, TIFF, WEBM... /b></li>
    <li><b>There currently exists functions for reading: 8-bit colour and greyscake, 12-bit, 16-bit, 24-bit colour</b></li>
    <li><b>Downsampling algorithm with average downsampling intensity of 1 - 20 times</b></li>
    <li><b>Aspect-Ratio setting for wider image types</b></li>
  </ol>
</div>

<h3>Limitations</h3>
  <p>The ASCII converter currently does not support alpha conversion with 32-bit PNG images. Neither does it currently support more esoteric bit types such as 4-bit, 1-bit, 2-bit. GIF's are pending</p>
</div>
