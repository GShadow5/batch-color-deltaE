'''
   batchColorDE.py
   Batch calculates CIE76 DeltaE values from RGB values in csv files. I plan to add a
   CIE2000 DeltaE implementation in the future.
   by Nayan Sawyer
   started Jan 19 2022
   version 1.0.0 Jan 22 2022

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

      {0} - There is only one page 
      {1} In the RGBtoLab() function, the variable names in the XYZ to Lab section match the 
      variable names used on http://brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
      to make the code implementation more legible. 
'''
import numpy as np

def RGBtoLab(colorArray):
   # To convert RGB to XYZ a conversion matrix is required.
   # This one is for sRGB and is based on the D65 reference white.
   # For more information see above {0}
   RGBtoXYZ_D65_matrix = np.array([[0.4124564,0.3575761,0.1804375],
                                   [0.2126729,0.7151522,0.0721750],
                                   [0.0193339,0.1191920,0.9503041]])

   '''
      Scale RGB to pref for matrix multiplication
   '''
   # Scale RGB values between 0 and 1
   colorArray = colorArray / 255

   # Inverse sRGB companding
   colorArray = np.where((colorArray <= 0.04045) & (colorArray > 0.04045), colorArray / 12.92, ((colorArray + 0.055)/1.055) ** 2.4) 


   '''
      Matrix multiplication to produce XYZ format
   '''
   # Requires transposition because the color triads are row wise, not column wise in the csv format. 
   # This turns the tall, 3 wide matrix into a wide, 3 tall matrix so that the multiplication can take place,
   # then transposes it back for the later steps.
   colorArray = np.transpose(np.matmul(RGBtoXYZ_D65_matrix, np.transpose(colorArray)))
   #print("XYZ\n" + str(colorArray))


   '''
      Convert XYZ to Lab using D65 reference white {1}
   '''
   # Ref white in XYZ (D65)
   Xr = 0.950470
   Yr = 1.0
   Zr = 1.088830

   e = 0.008856
   k = 903.3

   # Get xr yr zr
   for i in range(len(colorArray)):
      colorArray[i][0] = colorArray[i][0] / Xr
      colorArray[i][1] = colorArray[i][1] / Yr
      colorArray[i][2] = colorArray[i][2] / Zr

   # get fx fy fz
   colorArray = np.where((colorArray > e), colorArray ** (1/3), (k * colorArray + 16) / 116)

   # get Lab
   for i in range(len(colorArray)):
      fx = colorArray[i][0]
      fy = colorArray[i][1]
      fz = colorArray[i][2]
      colorArray[i][0] = (116 * fy) - 16
      colorArray[i][1] = 500 * (fx - fy)
      colorArray[i][2] = 200 * (fy - fz)

   #print("\nLab\n" + str(colorArray))

   return(colorArray)

def CIE76DeltaE(sample, reference):
   out = []
   for i in range(len(sample)):
      out.append(((sample[i][0] - reference[i][0]) ** 2 + (sample[i][1] - reference[i][1]) ** 2 + (sample[i][2] - reference[i][2]) ** 2) ** (1/2))
   return out


'''
PROGRAM START
'''
verbose = True # Print extra information

# Digest csv
sample = np.genfromtxt(".\\demo_sample.csv",delimiter=',')
key = np.genfromtxt(".\\demo_key.csv",delimiter=',')

if verbose: print("sample\n" + str(sample))
if verbose: print("key\n" + str(key))

# Covert to Lab color space
sample = RGBtoLab(sample)
key = RGBtoLab(key)

if verbose: print("\nLab sample\n" + str(sample))
if verbose: print("Lab key\n" + str(key))

# Output the DeltaE for each pair
print("\nDeltaE")
for i in CIE76DeltaE(key,sample):
   print(i)