data values;
length stage $20;
format money dollar8.;
order = _N_;
dummycat=1;
input stage &$ money;
datalines;
Round One Questions  17800
Round One Daily Double  17800
Round Two Questions  35200
Round Two DD1  70800
Round Two DD2  141600
Final Jeopardy  283200
;;;;
run;

title "Maximum Possible Jeopardy Winnings, By Round";
proc sgplot data=values;
vbarparm category=dummycat response=money/group=stage x2axis
         bardiwth=1.0 discreteoffset=-0.08 groupdisplay=stack ;
waterfall category=stage response=money/datalabel finalbartickvalue="Total";
x2axis display=none;
run;
