import numpy as np

def haar_sample_su2():
    """
    Generate a random SU(2) unitary (Haar measure).
    Returns a 2x2 complex unitary matrix.
    """
    # random quaternion
    u1, u2, u3 = np.random.normal(size=3)
    norm = np.sqrt(u1**2 + u2**2 + u3**2)
    u1, u2, u3 = u1/norm, u2/norm, u3/norm

    # convert to SU(2) matrix
    a = u1 + 1j*u2
    b = u3
    return np.array([[a, b], [-b, np.conj(a)]])

def rotate_z_by(u):
    """
    Apply SU(2) rotation u to z-axis vector.
    Returns rotated 3D unit vector.
    """
    # Pauli matrices
    sigma_x = np.array([[0,1],[1,0]])
    sigma_y = np.array([[0,-1j],[1j,0]])
    sigma_z = np.array([[1,0],[0,-1]])

    # Bloch representation of z-axis
    rho = (np.eye(2) + sigma_z) / 2
    rho_rot = u @ rho @ u.conj().T

    x = np.real(np.trace(rho_rot @ sigma_x))
    y = np.real(np.trace(rho_rot @ sigma_y))
    z = np.real(np.trace(rho_rot @ sigma_z))
    return np.array([x,y,z])

def phi(u):
    """
    Anisotropy function with zero mean over SU(2).
    For demo purposes, we use trace-based variant.
    """
    return np.real(np.trace(u)) - 0.5 # mean-zero tweak

def oir_correlator(axes, eps=0.0, M=10000):
    """
    Orientation Integral Rule (OIR) correlator.
    
    Parameters
    ----------
    axes : list of np.array
        List of analyzer directions (3D unit vectors).
    eps : float
        Anisotropy parameter (ε).
    M : int
        Number of Monte Carlo samples.
    
    Returns
    -------
    float : estimated correlator value.
    """
    acc = 0.0
    for _ in range(M):
        u = haar_sample_su2()
        n = rotate_z_by(u)
        val = 1.0
        for a in axes:
            c = np.dot(a, n)
            val *= (2*c*c - 1)
        w = 1 + (eps**2) * phi(u) # modulation
        acc += w * val
    return acc / M
