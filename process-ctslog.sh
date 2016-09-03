#!/bin/sh

for x in `find . -name "*.zip"`; do y=`dirname $x`; z=`basename $x .zip`; cd $y; mkdir $z; mv $z.zip $z; cd -; done
for x in `find . -name "*.zip"`; do cd `dirname $x`; 7z x `basename $x`; cd -; done
for x in `find . -name "*.zip"`; do rm $x; done

