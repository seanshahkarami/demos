#include <petscdmda.h>
#include <petscsnes.h>


PetscErrorCode FormFunction(SNES snes, Vec u, Vec f, void *user)
{
    DM dm;
    DMDALocalInfo info;
    PetscScalar **U;
    PetscScalar **F;
    Vec localU;

    SNESGetDM(snes, &dm);
    DMDAGetLocalInfo(dm, &info); // Indicates things like which blocks of a vector are availible to the local process?

    // Get data availible to local process?
    DMGetLocalVector(dm, &localU);
    DMGlobalToLocalBegin(dm, u, INSERT_VALUES, localU);
    DMGlobalToLocalEnd(dm, u, INSERT_VALUES, localU);

    DMDAVecGetArrayDOF(dm, localU, &U);
    DMDAVecGetArrayDOF(dm, f, &F);

    F[0][0] = 4*U[0][0]*U[0][0] + U[0][1]*U[0][1] - 1.0;
    F[0][1] = U[0][0]*U[0][0] + 9*U[0][1]*U[0][1] - 1.0;

    DMDAVecRestoreArrayDOF(dm, u, &U);
    DMDAVecRestoreArrayDOF(dm, f, &F);

    return 0;
}


int main(int argc, char **argv)
{
    DM dm;
    SNES snes;
    Vec u;
    Vec f;

    PetscInitialize(&argc,
                    &argv,
                    "options",
                    "Example of using DMDA with a 1D Field with 2 DOFs \
                    per node. Computes intersection of two ellipses.");

    SNESCreate(PETSC_COMM_WORLD, &snes);

    // Create a 1D field with 2 DOFs at 1 node. (Basically a field over a single point...)
    DMDACreate1d(PETSC_COMM_WORLD, DM_BOUNDARY_NONE, 1, 2, 1, PETSC_NULL, &dm);

    DMCreateGlobalVector(dm, &u);
    VecDuplicate(u, &f);

    SNESSetFunction(snes, f, FormFunction, NULL);
    SNESSetDM(snes, dm);
    SNESSetFromOptions(snes);

    VecSet(u, 0.35); // Initial guess.
    SNESSolve(snes, NULL, u);

    VecView(u, 0);

    VecDestroy(&u);
    VecDestroy(&f);
    SNESDestroy(&snes);
    DMDestroy(&dm);

    PetscFinalize();

    return 0;
}
