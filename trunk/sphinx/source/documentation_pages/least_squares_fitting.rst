==================================
Least squares fitting procedures
==================================

--------------
Algorithm
--------------

Define **S** matrix and **E** matrix which are N*3 matrix, and the N is the number of coordinates. 
**s_ave** and **e_ave** are two vector which are the average of the cloumn of **S** matrix and **E** matrix. This process fitting the **S** coordinates to **E** coorinates.

First, construct a 3*3 covariance matrix **C** between **S** matrix and **E** matrix using the following formula:

.. math::
    C=\frac{1}{N-1}(S^T  E - \frac{1}{N} S^T  I  I^T  E)

Here **I** is an N*1 column vector consisting of only ones.

From the nine elements of **C**, we subsequently generate the 4*4 real symmetric matrix **M** using the expression:

.. math::
    M=
    \begin{vmatrix}
    c_{11}+c_{22}+c_{33} & c_{23}-c_{32}         &  c_{31}-c_{13}        & c_{12}-c_{21} \\ 
    c_{23}-c_{32}        & c_{11}-c_{22}-c_{33}  &  c_{12}+c_{21}        & c_{31}+c_{13} \\ 
    c_{31}-c_{13}        & c_{12}+c_{21}         & -c_{11}+c_{22}-c_{33} & c_{23}+c_{32} \\ 
    c_{12}-c_{21}        & c_{31}+c_{13}         &  c_{23}+c_{32}        & -c_{11}-c_{22}+c_{33} \\ 
    \end{vmatrix}


The (:math:`q_1,q_2,q_3,q_4`) is the eigenvector corresponding to the largest eigenvalue of matrix **M**. Using the element of the largest eigenvector, the orientation matrix **R** can be established by equation below:

.. math::
    R=
    \begin{vmatrix}
    q_0q_0+q_1q_1-q_2q_2-q_3q_3  &  2(q_1q_2 - q_0q_3)           & 2(q_1q_3+q_0q_2) \\
    2(q_2q_1+q_0q_3)             &  q_0q_0-q_1q_1+q_2q_2-q_3q_3  & 2(q_2q_3-q_0q_1) \\
    2(q_3q_1-q_0q_2)             &  2(q_3q_2 + q_0q_1)           & q_0q_0-q_1q_1- q_2q_2+q_3q_3 \\
    \end{vmatrix}

The first column of matrix **R** corresponds to x-axis of the base, the second to y-axis, and the third to z-axis.

The origin coordinate of the base can be calculated using equation below:

.. math::
    O=E_{ave}-S_{ave}R^{T}

The :math:`E_{ave}` is the vector of the average of experimental coordinates, 
and the :math:`S_{ave}` is the vector corresponding to the average of the standard coordinates of base.

Now the fitting coordinates can be calculate from the rotation matrix **R** and origin **o** using the formula below:

.. math::
    F=SR^T+o

The upper algorithm consulted the 3DNA software package.



