# Disorderly Escape
## Problem

Oh no! You've managed to free the bunny workers and escape Commander Lambdas exploding space station, but Lambda's team of elite starfighters has flanked your ship. If you dont jump to hyperspace, and fast, you'll be shot out of the sky!

Problem is, to avoid detection by galactic law enforcement, Commander Lambda planted the space station in the middle of a quasar quantum flux field. In order to make the jump to hyperspace, you need to know the configuration of celestial bodies in the quadrant you plan to jump through. In order to do *that*, you need to figure out how many configurations each quadrant could possibly have, so that you can pick the optimal quadrant through which youll make your jump. 

There's something important to note about quasar quantum flux fields' configurations: when drawn on a star grid, configurations are considered equivalent by grouping rather than by order. That is, for a given set of configurations, if you exchange the position of any two columns or any two rows some number of times, youll find that all of those configurations are equivalent in that way -- in grouping, rather than order.

Write a function solution(w, h, s) that takes 3 integers and returns the number of unique, non-equivalent configurations that can be found on a star grid w blocks wide and h blocks tall where each celestial body has s possible states. Equivalency is defined as above: any two star grids with each celestial body in the same state where the actual order of the rows and columns do not matter (and can thus be freely swapped around). Star grid standardization means that the width and height of the grid will always be between 1 and 12, inclusive. And while there are a variety of celestial bodies in each grid, the number of states of those bodies is between 2 and 20, inclusive. The solution can be over 20 digits long, so return it as a decimal string.  The intermediate values can also be large, so you will likely need to use at least 64-bit integers.

For example, consider w=2, h=2, s=2. We have a 2x2 grid where each celestial body is either in state 0 (for instance, silent) or state 1 (for instance, noisy).  We can examine which grids are equivalent by swapping rows and columns.
```
00
00
```
In the above configuration, all celestial bodies are "silent" - that is, they have a state of 0 - so any swap of row or column would keep it in the same state.
```
00 00 01 10
01 10 00 00
```
1 celestial body is emitting noise - that is, has a state of 1 - so swapping rows and columns can put it in any of the 4 positions.  All four of the above configurations are equivalent.
```
00 11
11 00
```
2 celestial bodies are emitting noise side-by-side.  Swapping columns leaves them unchanged, and swapping rows simply moves them between the top and bottom.  In both, the *groupings* are the same: one row with two bodies in state 0, one row with two bodies in state 1, and two columns with one of each state.
```
01 10
01 10
```
2 noisy celestial bodies adjacent vertically. This is symmetric to the side-by-side case, but it is different because there's no way to transpose the grid.
```
01 10
10 01
```
2 noisy celestial bodies diagonally.  Both have 2 rows and 2 columns that have one of each state, so they are equivalent to each other.
```
01 10 11 11
11 11 01 10
```
3 noisy celestial bodies, similar to the case where only one of four is noisy.
```
11
11
```
4 noisy celestial bodies.

There are 7 distinct, non-equivalent grids in total, so solution(2, 2, 2) would return 7.

---

### Test cases
Your code should pass the following test cases.Note that it may also be run against hidden test cases not shown here.

- Python cases 
```
Input:solution.solution(2, 3, 4)
Output:    430
```
```
Input:solution.solution(2, 2, 2)
Output:    7
```

## Solution
Upon receiving this problem, I immediately dismissed the idea of brute-forcing $20^{10000}$ cases as it seemed impractical. It became evident that simple math operations and logic comparisons wouldn't suffice, ruling out the possibility of using Dynamic Programming as well. In this moment of uncertainty, I turned to the guiding light of Google Search, which led me to discover Burnside's Lemma and necklace problem. 

As Burnside's Lemma (possibly not Burnside's) stated, given a set $X$ representing the set of states, and a set of group actions $G$ (e.g. rotations of elements in a rows), the formula for determining the number of final orbit sets is: 
    
$$N = \frac{1}{|G|} \sum_{g \in G} |X^g|$$
, in which $X^g$ denotes the set of elements in $X$ that is unchanged under the action $g$. 

Consider the necklace problem, which involves counting the number of distinct necklaces that can be formed using a set of beads, considering that rotations and reflections of the same necklace are considered identical. For example, let's consider a necklace with a length of 4, where each bead can have 2 states: 0 and 1. In this case, we have 4 types of rotations, hence, $|G| = 4$ (as 5-rotation would similar to shifting 4 then shifting 1):
- $g_1$ (1-rotation): Shifting the necklace by 1 bead, we realize that only 0000 and 1111 would not change, so the size of $X^{g_1}$ is 2. 
- $g_2$ (2-rotation): Shifting the necklace by 2 beads (eg: 0011 -> 0110) results in 4 strings that remain unchanged $X^{g_2}= {0000, 0101, 1010, 1111}$.
- $g_3$ (3-rotation): Again, this rotation results in only 0000 and 1111 remaining unchanged.
- $g_4$ (4-rotation): This rotation would leave all 16 permutations of the length-4 necklace unchanged, hence $|X^{g_4}| = 16$. 

Finally, we would have the number of symmetric groups to be: 
$$N = \frac{1}{4}*(2+4+2+16) = 6$$
This leaves the group representations as ${0000,0001,0011,0111,1010,1111}$. Remember, these are the **representations** of the group that remain unchanged under certain shifts, not the number of unchanged **permutations**.

To turn this into programmable code, we need to make some mathematical conversions, but I'll try to keep it as intuitive as possible.

Let's consider the string "0011" and try to repeat it using a 3-bit left shift (3-rotation). Here's the process:
```
i = 0: s = {0}011
i = 1: s = 1{0}01
i = 2: s = 11{0}0
i = 3: s = 011{0}
i = 4: s = {0}011
```
The element in curly brackets represents the 1st element for easy tracking. We observe that the string repeats itself after 4 loops. This repetition is called a cycle, and the number of loops is the cycle's length. According to this [Wiki page](https://en.wikipedia.org/wiki/Least_common_multiple#Gears_problem), the cycle's length can be calculated using the formula $\frac{lcm(i, |G|)}{i}$.

Now, imagine you have a large string with length $G$ and a small string with length $L$ ($0<L<G$, and $G\%L=0$). How many small strings does it take to fit the length of the large string? It's $\frac{G}{L}$, right?

Using the same logic, if we have a permutation of length $n = |G|$, and each cycle has a length of $\frac{lcm(i,n)}{i}$, then the number of cycles in each permutation would be $\frac{n*i}{lcm(i,n)}$. Fortunately, this is equivalent to the formula for calculating the greatest common divisor (gcd) of $i$ and $n$. Hence, the number of cycles is $gcd(i, n)$.

Without considering the structure of the permutation, we observe that each cycle has $s$ choices of states. Since each cycle is independent, we can multiply the choices to obtain the final number of choices for the rotation, which is $s^{gcd(i,n)}$. Finally, we have a programmable formula like this:

$$N = \frac{1}{|G|}\sum_{i=1}^{|G|}s^{gcd(i, |G|)}$$

Returning to the problem at hand, we are dealing with a matrix, not just a string, which means we must take into consideration the permutations within the matrix itself. I was initially believe that multiplying the formulas for rows and columns would suffice. However, this approach fails to account for the permutation within the matrix as a product of two distinct permutation groups (one for rows and one for columns). To overcome this limitation, a more powerful tool is required: calculating the cycle index of the direct product of permutation groups.

I recommend reading the article [here](https://franklinvp.github.io/2020-06-05-PolyaFooBar/) for a thorough understanding. In case you encounter any scrolling issues, you can open the inspector and modify the CSS of the navigation bar by setting its position to either absolute or relative, depending on what suits your monitor.

Finally, in Foobar, the use of the math library in Python is restricted for this problem. Hence, writing your own functions to calculate the gcd and factorial would be necessary to avoid some issues with the public test cases when verifying your solution on Foobar.
