import numpy as np
import sympy as sp

def format_complex(num):
    """Format complex number for display."""
    if abs(num.imag) < 1e-10:
        return f"{num.real:.6f}".rstrip('0').rstrip('.')
    else:
        real_part = f"{num.real:.6f}".rstrip('0').rstrip('.')
        imag_part = f"{abs(num.imag):.6f}".rstrip('0').rstrip('.')
        if num.imag >= 0:
            return f"{real_part} + {imag_part}i"
        else:
            return f"{real_part} - {imag_part}i"

def solve_custom_recurrence_advanced():
    print("\n" + "=" * 50)
    print("ADVANCED CUSTOMIZABLE RECURRENCE RELATION SOLVER")
    print("=" * 50)
    print("For recurrence relation: a*a_n + b*a_{n-1} + c*a_{n-2} = 0")
    print()
    
    try:
        # Get coefficients
        print("STEP 1: Enter the coefficients")
        print("-" * 50)
        
        # Option to use default or custom values
        use_default = input("Use default example (a_n + 5a_{n-1} + 6a_{n-2} = 0)? (y/n): ")
        
        if use_default.lower() != 'n':
            a, b, c = 1, 5, 6
        else:
            a = sp.sympify(input("Enter coefficient a (for a_n): ") or "1")
            b = sp.sympify(input("Enter coefficient b (for a_{n-1}): "))
            c = sp.sympify(input("Enter coefficient c (for a_{n-2}): "))
        
        # Normalize coefficients
        if a == 0:
            raise ValueError("Coefficient 'a' cannot be zero (not a second-order recurrence)")
        
        b_norm = b / a
        c_norm = c / a
        
        print(f"\nNormalized recurrence relation: a_n + {b_norm}a_{{n-1}} + {c_norm}a_{{n-2}} = 0")
        
        # Get initial conditions
        print("\nSTEP 2: Enter initial conditions")
        print("-" * 50)
        
        use_default_ic = input("Use default initial conditions (a_0 = 0, a_1 = 1)? (y/n): ")
        
        if use_default_ic.lower() != 'n':
            a0, a1 = 0, 1
        else:
            a0 = sp.sympify(input("Enter a_0: "))
            a1 = sp.sympify(input("Enter a_1: "))
        
        print(f"\nInitial conditions: a_0 = {a0}, a_1 = {a1}")
        
        # Get number of terms
        n_terms = int(input("\nHow many terms to calculate? (default 15): ") or "15")
        n_terms = max(2, min(n_terms, 30))
        
        # Solve using SymPy for exact symbolic solutions
        print("\n" + "=" * 50)
        print("SOLUTION PROCESS (SYMBOLIC)")
        print("=" * 50)
        
        # Step 1: Find characteristic polynomial
        print("STEP 1: Find the characteristic polynomial")
        r = sp.Symbol('r')
        char_poly = r**2 + b_norm*r + c_norm
        print(f"Characteristic polynomial: {char_poly} = 0")
        
        # Step 2: Find the roots symbolically
        print("\nSTEP 2: Find the roots")
        roots = sp.solve(char_poly, r)
        
        if len(roots) == 2:
            r1, r2 = roots
            print(f"Root 1 (r₁) = {r1}")
            print(f"Root 2 (r₂) = {r2}")
            
            # Check if roots are equal (repeated roots)
            repeated_roots = (r1 == r2)
            
            # Step 3: Form general solution
            print("\nSTEP 3: Form the general solution")
            n = sp.Symbol('n')
            
            if repeated_roots:
                print("Since we have a repeated root, the general solution is:")
                general_solution = sp.Function('A')(n) * (r1**n) + sp.Function('B')(n) * n * (r1**n)
                print(f"a_n = A({r1})^n + Bn({r1})^n")
            else:
                print("Since we have distinct roots, the general solution is:")
                general_solution = sp.Function('A')(n) * (r1**n) + sp.Function('B')(n) * (r2**n)
                print(f"a_n = A({r1})^n + B({r2})^n")
            
            # Step 4: Apply initial conditions
            print("\nSTEP 4: Apply initial conditions to find A and B")
            
            A, B = sp.symbols('A B')
            
            if repeated_roots:
                # For repeated roots: a_0 = A, a_1 = A*r1 + B
                eq1 = sp.Eq(A, a0)
                eq2 = sp.Eq(A*r1 + B, a1)
            else:
                # For distinct roots: a_0 = A + B, a_1 = A*r1 + B*r2
                eq1 = sp.Eq(A + B, a0)
                eq2 = sp.Eq(A*r1 + B*r2, a1)
            
            print(f"Equation 1: {eq1}")
            print(f"Equation 2: {eq2}")
            
            # Solve for A and B
            solution = sp.solve([eq1, eq2], [A, B])
            
            if solution:
                A_val = solution[A]
                B_val = solution[B]
                
                print(f"\nSolution:")
                print(f"A = {A_val}")
                print(f"B = {B_val}")
                
                # Step 5: Write explicit formula
                print("\nSTEP 5: Write the explicit formula")
                
                if repeated_roots:
                    explicit_formula = f"a_n = {A_val}({r1})^n + {B_val}n({r1})^n"
                else:
                    explicit_formula = f"a_n = {A_val}({r1})^n + {B_val}({r2})^n"
                
                print(f"Explicit formula: {explicit_formula}")
                
                # Step 6: Calculate sequence
                print(f"\nSTEP 6: Calculate the first {n_terms} terms")
                print("-" * 50)
                
                sequence = []
                
                # Convert symbolic expressions to numerical values for calculation
                A_numeric = complex(A_val.evalf())
                B_numeric = complex(B_val.evalf())
                
                if repeated_roots:
                    r1_numeric = complex(r1.evalf())
                    
                    for i in range(n_terms):
                        term = A_numeric * (r1_numeric**i) + B_numeric * i * (r1_numeric**i)
                        
                        # Convert to real if imaginary part is negligible
                        if abs(term.imag) < 1e-10:
                            term = term.real
                            
                        sequence.append(term)
                        print(f"a_{i:2d} = {format_complex(term) if isinstance(term, complex) else term}")
                else:
                    r1_numeric = complex(r1.evalf())
                    r2_numeric = complex(r2.evalf())
                    
                    for i in range(n_terms):
                        term = A_numeric * (r1_numeric**i) + B_numeric * (r2_numeric**i)
                        
                        # Convert to real if imaginary part is negligible
                        if abs(term.imag) < 1e-10:
                            term = term.real
                            
                        # Convert to integer if very close to an integer
                        if isinstance(term, float) and abs(term - round(term)) < 1e-10:
                            term = int(round(term))
                            
                        sequence.append(term)
                        print(f"a_{i:2d} = {format_complex(term) if isinstance(term, complex) else term}")
            
                # Final summary
                print("\n" + "=" * 50)
                print("FINAL SUMMARY")
                print("=" * 50)
                print(f"Recurrence relation: a_n + {b_norm}a_{{n-1}} + {c_norm}a_{{n-2}} = 0")
                print(f"Initial conditions: a_0 = {a0}, a_1 = {a1}")
                print(f"Characteristic roots: r₁ = {r1}, r₂ = {r2}")
                print(f"Constants: A = {A_val}, B = {B_val}")
                print(f"Explicit formula: {explicit_formula}")
                print(f"First few terms: {[sequence[i] for i in range(min(10, n_terms))]}")
                
                return {
                    'coefficients': (a, b, c),
                    'normalized_coefficients': (1, b_norm, c_norm),
                    'initial_conditions': (a0, a1),
                    'roots': (r1, r2),
                    'constants': (A_val, B_val),
                    'sequence': sequence
                }
            else:
                print("Error: Could not solve for constants A and B.")
                return None
        else:
            print(f"Error: Expected 2 roots, but found {len(roots)}.")
            return None
            
    except ValueError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return None

# Main execution
if __name__ == "__main__":
    solution = solve_custom_recurrence_advanced()
    
    if solution:
        # Ask if user wants to try another recurrence relation
        try_again = input("\nWould you like to solve another recurrence relation? (y/n): ")
        if try_again.lower() == 'y':
            solve_custom_recurrence_advanced()
