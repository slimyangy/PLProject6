# PLProject6

##Problem 1:

###test cases:

(let (fred 12) (+ fred 1))
> variable "fred" value does get cleared
> returns 13

fred
> returns fred

(let (a 1))
> just assigns a with value 1
> retains its value until used in "(let (x 1)(+ x 1))"-like format

a
> returns 1

(+ a 3)
> returns 4

(- a 3)
> returns -2

(* a 3)
> returns 3

(/ a 3)
> returns 0.333333

(/ a 0)
> returns error message

(if #f 10 13)
> returns 13

(if #t 21 13)
> returns 21

###extra notes:
> +, -, /, * all supported
> variable clearing done as specified

##Problem 2:

###test case:

(car '(1 2 3))

###extra notes:
> we just did what professor Cannata did in class
