-- A minimal regular expression matcher inspired by Rob Pike's TPOP exercises.

match ('^':rs) xs = matchhere rs xs
match (r:rs) (x:xs) = (matchhere (r:rs) (x:xs)) || (matchhere rs xs)

matchhere [] _ = True
matchhere ('$':[]) [] = True
matchhere (c:'*':rs) xs = matchstar c rs xs
matchhere ('.':rs) (x:xs) = matchhere rs xs
matchhere (c:rs) (x:xs) = (c == x) && (matchhere rs xs)
matchhere _ _ = False

matchstar c re (x:xs) = (matchhere re (x:xs)) || ((matchchar c x) && (matchstar c re xs))
matchstar _ _ [] = False

matchchar '.' _ = True
matchchar c x = c == x

main = print $ match "^ab*c$" "abbbbbbbbc"
