/* sample.sas - Sample SAS script for testing metadata extraction */

%macro sample_macro(param1);
    %let local_var = &param1;
    data temp_dataset;
        set sashelp.class;
        where age > 12;
    run;

    proc print data=temp_dataset;
    run;
%mend sample_macro;

libname mylib 'C:\temp';

data mylib.my_dataset;
    input id name $ age;
    datalines;
1 John 25
2 Jane 30
;
run;

%sample_macro(hello);
