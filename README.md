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
      <li>Download -> Source Code || .exe</li>
      <li>Parameters & Examples</li>
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
  <p>This repository aims to explore the process of Image to ASCII conversion without reliance on external Python libraries. The only dependencies include:</p>
  <ol>
    <li><b>'import os' to allow direct communication with file status using operating system, allows case checking for valid i/o paths</b></li>
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
      <li><b>Negative or Positive ASCII mode. Either "light" or "dark" -> Inverts shadows, view below:</b></li>
  </ol>
</div>

<h3>Limitations</h3>
  <p>The ASCII converter currently does not support alpha conversion with 32-bit PNG images. Neither does it currently support more esoteric bit types such as 4-bit, 1-bit, 2-bit. GIF's are pending</p>
</div>

<h1>How to Setup</h1>

<div>
  <h3>Download -> Source Code || .exe</h3>
  <p>Observe below the contents of ASCII_Converter:</p>
  <ul>
    <li><b>It's first two folders consist of build data for the pyinstaller executable, and the folder containing the executable program for the code and reliable location for placing your images</b></li>
    <li><b>There are two ASCII_Converter source files in jupyter notebook and python, both may be preferable if you wish to modify any functionalities directly</b></li>
    <li><b>A readme containing a copy of the Github's repository README</b></li>
  </ul>

  <p><b>If you wish to directly run the application, simply place a folder inside of IMG'S_HERE, open the ASCII_Converter, and after conversion, an output file will be specified. More on command line instructions for .exe converter below</b></p>
</div>

<div>
  <h3>Parameters & Examples</h3>
  <p>Observe below the contents of ASCII_Converter.exe:</p>
  <ul>
    <p>The .exe will prompt the user to provide a correct input in regards to each step (either required or optional), for the ASCII conversion process.</p>
    <li><b>Example, if your image is called Test, and is a .jpg file, you would respond to the first query with -> Test.jpg</b></li>
    <p>You will then be asked what your prefered downsampling factor will be. Larger images benefit from hi  gher downsampling, with bullpark values usually in the range of 5-20 (Experiment as you see fit)</p>
    <li><b>Example, you could provide a value 5 -> downsamples the image by 5 times its original size</b></li>
    <p>You will then be asked If you would like to specifiy an aspect ratio. This determines the width to height ratio of an image, as ASCII tends to be visually taller than wider, it can be beneficial for detailed images</p>
    <li><b>Example, if you would like a double 2:1 aspect ratio, input -> 2</b></li>
    <p>You will then be asked if you would like to specify whether the image uses negative shadows or its default postive ones.</p>
    <li><b>Example, by default, ASCII is outputted as light shadow mode, but can be specified to dark. Input the word light, or dark for these modes-> 2</b></li>
  </ul>

  <p>CONGRATULATIONS, you have now created a notepad.txt file called output, that will have contained your specified ASCII text based on the input image. <b>WARNING: Additional conversions will overwrite this file, so take care to backup each ASCII you create</b></p>
</div>

<div>
  <h3>Creating your own Executable!</h3>
  <ol>
    <li><b>To create your own executable, all you need is to download the notebook version of the ASCII_Converter as specified above (.ipynb).</b></li>
    <li>Open cmd</b></li>
    <li>Right click the file explorer top repository bar to grab the location path where your file resides</b></li>
    <li>Chose copy</li>
    <li>add cd to your windows cmd and paste the repository path in as follows:</li>
    <li>In the correct path, add the following line to create a .py copy of your ASCII_Converter</li>
    Inline 'cmd'
  ```jupyter nbconvert --to script ASCII_Converter.ipynb```
  <li>Wait until the file is created, than create an executable using the following line</li>
    Inline 'cmd'
  ```pyinstaller --onefile ascii_converter.py```

  <li>Your executable will now be available in the dist folder!</li>
  </ol>
  
