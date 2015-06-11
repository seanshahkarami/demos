#include <petscsnes.h>


typedef struct
{
    PetscScalar a;
    PetscScalar b;
} MyContext;


PetscErrorCode FormFunction(SNES snes, Vec x, Vec f, void *ctx)
{
    MyContext *info = (MyContext *)ctx;
    const PetscScalar *X;
    PetscScalar *F;

    VecGetArrayRead(x, &X);
    VecGetArray(f, &F);

    F[0] = info->a*X[0]*X[0] + X[1]*X[1] - 1;
    F[1] = X[0]*X[0] + info->b*X[1]*X[1] - 1;

    VecRestoreArrayRead(x, &X);
    VecRestoreArray(f, &F);

    return 0;
}


int main(int argc, char **argv)
{
    SNES snes;
    Vec f;
    Vec x;

    MyContext ctx;
    ctx.a = 4.0;
    ctx.b = 9.0;

    PetscInitialize(&argc, &argv, "options", "My first PETSc program.");

    VecCreateSeq(PETSC_COMM_WORLD, 2, &f);

    PetscScalar X[] = {0.48, 0.29};
    VecCreateSeqWithArray(PETSC_COMM_WORLD, 1, 2, X, &x);

    SNESCreate(PETSC_COMM_WORLD, &snes);
    SNESSetFunction(snes, f, FormFunction, &ctx);
    SNESSetFromOptions(snes);
    SNESSolve(snes, NULL, x);

    VecView(x, PETSC_VIEWER_STDOUT_WORLD);

    VecDestroy(&f);
    VecDestroy(&x);
    SNESDestroy(&snes);

    PetscFinalize();

    return 0;
}
