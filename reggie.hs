data RE = Cat RE RE | Plus RE RE | Star RE | Neg RE | Sym Char | Empty | None
    deriving (Show, Eq)

cat :: RE -> RE -> RE
cat r Empty = r
cat Empty s = s
cat None _ = None
cat _ None = None
cat r s = Cat r s

plus :: RE -> RE -> RE
plus _ Empty = Empty
plus Empty _ = Empty
plus r None = r
plus None s = s
plus r s = Plus r s

star :: RE -> RE
star Empty = Empty
star None = Empty
star r = Star r

neg :: RE -> RE
neg Empty = None
neg None = Empty
neg r = Neg r

nullable :: RE -> RE
nullable Empty = Empty
nullable None = None
nullable (Sym _) = None
nullable (Plus r s) = plus (nullable r) (nullable s)
nullable (Star _) = Empty
nullable (Neg r) = neg (nullable r)

deriv :: Char -> RE -> RE
deriv a Empty = None
deriv a None = None
deriv a (Sym b) = if a == b then Empty else None
deriv a (Cat r s) = plus (cat (deriv a r) s)
                         (cat (nullable r) (deriv a s))
deriv a (Star r) = cat (deriv a r) (star r)
deriv a (Plus r s) = plus (deriv a r) (deriv a s)
deriv a (Neg r) = neg (deriv a r)

derivs :: [Char] -> RE -> RE
derivs [] r = r
derivs (a:as) r = derivs as (deriv a r)

match :: [Char] -> RE -> Bool
match as r = nullable (derivs as r) == Empty

main = print $ match "ab" (star (cat (Sym 'a') (Sym 'b')))
