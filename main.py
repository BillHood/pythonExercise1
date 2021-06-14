# By Bill Hood on June 9-10, 2021
# In consideration of employment - this is my sample code
# The instructions: Candidate should write a program that reads a list of numbers and for each number estimates
#  the running mean,running Standard Deviation and running median and prints out the results per data point
# Notes:Input is Standard In being one number per line
#       This code is Python3 using Numpy as a module which by default uses a biased estimator for Standard Deviation
#       All Standard Deviation calculations are therefore, are biased in nature
#       Numpy by default calculates Median as follows:
#           Median calculations with odd numbered data points will be the natural median - middle value of a sorted list
#           Median calculations with even numbered data points will be the average of the two middle values
#       Data Input read programming is resilient to malformed data and checks
#           the line to see if it contains a numeric value via two seperate tests. The code looks for lines of data
#           containing a numeric and equally looks at and dismisses any line containing non-numeric charactor(s)
#       Numpy was chosen for a number of reasons most noteably support of Arrays rather than Python lists
#       This code is very fast processing 100,000 records at 64bit precision in less than 2 minutes
#       To see any significant impact on performance the programmer would need to select 128bit and run against
#       large data sets of 20,000 or more.
#
#       Code includes a utility that writes at a test file with random data and then may be feed into the software
# Imports
import numpy as np
import random
import datetime

# These are program variables you can set to an initial value
# Bill adds lower m to designate his variables and make them easy to see in code
mCount = 0
mDataCount = 0
mMakeData = 1               # 1 for on anything else for off
mRecs = 20000               # number test records
mRunningMean = 0
mRunningSTD = 0
mRunningMedian = 0
mRandomRangeStart = 1       # Random Number Start Range
mRandomRangeEnd = 5         # Random Number End Range

# make some sample data - not in the specs - but sure is handy!
if mMakeData == 1:                              # mMakeData is a flag and 1 is on - else is off
    fw = open("TestData20.txt", "w")            # Open a file for over write

    for i in range(1, mRecs + 1):               # recs is a user defined variable - 20000 runs fast
        x = float(random.randrange(mRandomRangeStart, mRandomRangeEnd))
        fw.write(str(x) + chr(10))              # write the data
    fw.close()                                  # close the file

# These are the program variables you can alter for control
mDataSet = "TestData02.txt" # this can be changed to the file you want to examine
                            # TestData20.txt is the file created by the random number generator
                            # other valid files included are Data01.txt, TestData01.txt, Data02.txt,
                            # and TestData03.txt
                            # use ATaleOfTwoCities.txt to run this against the actual book :)
                            # Use TestData02.txt for the dataset referenced in your email
mPrecision0 = ".0f"         # Used to control how the data is formatted when displayed - 0 decimals in this case
mPrecision4 = ".4f"         # Used to control how the data is formatted when displayed - 4 decimals in this case
mPrecision6 = ".6f"         # and so on
mPrecision8 = ".8f"
mPrecision12 = ".12f"
mFloatType = "float64"      # you can choose from float16, float32, float64 or float128
                            # with float128 yielding the slowest run times & most precision followed by float64, 32, 16
                            # float64 is recomended since it yields reasonably fast run times with good precision
                            # try float128 for some exagrated run times
                            # this will be used to create the array in a numerical format we select
# These are static system variables
mF = open(mDataSet, "r")                 # open the file read only
mLines = mF.readlines()                  # lines is the number we read from the file
mCount = np.count_nonzero(mLines)        # and count - we keep track of the recs we found and how many were data
print(str(mCount) + " records initially counted")

mF.seek(0)                               # move back to the top of the file
mA = np.array([])                        # create the empty array
mA = mA.astype(mFloatType)               # set the floating type for the entire array for precision control
mBeginTime = datetime.datetime.now()     # mark the time to measure how long a run takes

for i in range(1, mCount + 1):           # run begins - main loop
    mDataLine = mF.readline().strip()    # read a line from the file and strip away any blank data that might be present

    if mDataLine.isnumeric():                   # valid data a line made up of a sequence of integers such as 1223
                                                # isnumeric is true when the data is one or more integers
                                                # data with a decimal point is handled later
                                                # If isnumeric is True - then
        mDataCount = mDataCount + 1                 # increment the counter for the new data row you have found
        mDataLine = int(mDataLine)                  # convert the string data to an integer data format

        mNewA = np.append(mA, [mDataLine], axis=0)  # append the new data to the existing data as a new row at bottom
        mA = mNewA                                  # With the new record added - make mA the main array again
                                                    # now calculate mean, median and sd and print to console
        mASorted = np.sort(mA)                      # sort the data you have so far to calculate median
        mRunningMean = np.mean(mA)                  # Mean calculation does not need to use sorted data - so we use mA
        mRunningSTD = np.std(mA)                    # STD calculation does not need to use sorted data - so we use mA
        mRunningMedian = np.median(mASorted)        # Median can only be calculated by examining sorted data - so we
                                                    # use mASorted
                                                    # This code is duplicated in the second test and could be
                                                    # consolidated to a def call for ease of maintenance




    else :                                                  #Else control passes to here because the line contains
                                                            # a non-numeric such as a period
                                                            # or other non-numeric charactor such as a,b,c,....%,#,@,!..
                                                            # we can try to force a conversion to floating point and
                                                            # if the data is 1.12 or 2.31 or any sort of numeric
                                                            # and decimal combination- it will convert - otherewise
                                                            # a line with any letter - will not convert and will
                                                            # Except and loops out
        try:                                                # Try to convert the data into a floating point number
            mDataForce = float(mDataLine)                   # if you can perform this calculation without Exception-
                                                            # the next line executes - it is because the the data
                                                            # converted to a floting point numeric
                                                            #
            mDataCount = mDataCount + 1                     # like above - increment the data count
            mDataLine = float(mDataLine)                    # convert data to floating point numeric
            mNewA = np.append(mA, [mDataLine], axis=0)      # append new data to existing data
            mA = mNewA                                      # rename back to mA
            mASorted = np.sort(mA)                          # create a sorted version of array
            mRunningMean = np.mean(mA)                      # calculate Mean on mA
            mRunningSTD = np.std(mA)                        # calculate STD on mA
            mRunningMedian = np.median(mASorted)            # calculate median on mASorted
        except:                                             # If we get here - the data has failed two tests and is not numeric
            print(mDataLine + " fails decimal test")        # we do not increment the counter, we do not add data to the array, we do not make any calculations
                                                            # print out the running mean,std, and median
    # This line is after the main loop completes one pass and a handy place to print out summary data for that iteration
    print("Data Points " + str(format(mDataCount, mPrecision0)) + " R Mean " + str(format(mRunningMean, mPrecision4)) + " R STD " + str(format(mRunningSTD, mPrecision4)) + " R Median " + str(format(mRunningMedian,mPrecision4)))
# we have looped through all the data - now print summary info on the overall run
print("Dataset has " + str(format(mCount)) + " records, of which " + str(mDataCount) + " were numeric values and included in the calculations")
print((datetime.datetime.now() - mBeginTime))               # print the elapased time for the run
# end
# Thank you for the opportunity
# Bill's workstation: mac OS Big Sur on a MAC Mini Apple M1 chip
#
