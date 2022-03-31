# Batch Color DeltaE CIE76
## CIE2000 support planned for future

This is an implementation of the math on http://brucelindbloom.com for comparing
      a large number of RGB pairs using the CIE76 standard. All credit for the math goes to
      Bruce Lindbbloom and the Commission Internationale de l'Eclairage which defines the
      standards.

This program is fairly straight forward to use, however it does not sanitize the csv
      that you point it towards, so it is important to double check your files before use.
      The csv format to use is three integer RGB values seperated with commas, and a return
      character at the end of the line. This is the format output by google sheets when you
      export to csv. Like so

         162,101,45
         197,136,109
         221,221,217
         185,115,8
         187,145,20

The first RGB group on line 1 of the csv of the sample data set will be compared to
      the first RGB group on line 1 of the csv of the reference data set.

In the RGBtoLab() function, the variable names in the XYZ to Lab section match the
      variable names used on http://brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
      to make the code implementation more legible.
