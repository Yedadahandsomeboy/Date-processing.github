FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

convertToMeters 0.001;  

vertices
(
    (-100 -60  0)   // 0
    ( 160 -60  0)   // 1
    ( 160  60  0)   // 2
    (-100  60  0)   // 3
    (-100 -60  1)   // 4 (z方向极薄)
    ( 160 -60  1)   // 5
    ( 160  60  1)   // 6
    (-100  60  1)   // 7
);

blocks
(
    hex (0 1 2 3 4 5 6 7) (260 120 1) simpleGrading (1 1 1)  // 260x120x1 的网格
);

edges
(
);

boundary
(
    inlet
    {
        type patch;
        faces
        (
            (0 4 7 3)
        );
    }
    outlet
    {
        type patch;
        faces
        (
            (1 2 6 5)
        );
    }
    topBottom
    {
        type patch;
        faces
        (
            (3 7 6 2)
            (0 1 5 4)
        );
    }
    frontAndBack
    {
        type empty;
        faces
        (
            (0 3 2 1)
            (4 5 6 7)a
        );
    }
);

mergePatchPairs
(
);

// ************************************************************************* //
