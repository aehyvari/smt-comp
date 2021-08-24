SELECTION=final
export SELECTION

mkdir -p $SELECTION

./make_spaces.sh --include-nc --mv $SELECTION/mv.xml --uc $SELECTION/uc.xml --inc $SELECTION/inc.xml --sq $SELECTION/sq.xml --parallel $SELECTION/parallel.xml --cloud $SELECTION/cloud.xml

cd $SELECTION
for i in sq inc mv uc parallel cloud; do
   tar czf $i.tar.gz $i.xml
done
