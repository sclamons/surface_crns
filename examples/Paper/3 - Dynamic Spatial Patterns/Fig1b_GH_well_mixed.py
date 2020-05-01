import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
# mpl.rcParams['figure.dpi'] = 300

from matplotlib.font_manager import FontProperties
small_font = FontProperties()
small_font.set_size('small')

# Color cycling nonsense
import pylab
cm = pylab.get_cmap('viridis_r')

mpl.rc('text', usetex=False)
mpl.rc('xtick', labelsize=20)
mpl.rc('ytick', labelsize=20)
mpl.rc('axes', linewidth=1.75)
plt.rc('axes', labelsize=26)
plt.gcf().subplots_adjust(bottom=0.15)

dark_safe_colors = ["#1b9e77", "#d95f02", "#7570b3"]
light_safe_colors = ["#66c2a5", "#fc8d62", "#8da0cb"]

def simulate(system_dv_dt, params, state_inits, t_max, n_times):
    '''
    Run a scipy simulation. 
    
    Params:
        system_dv_dt: A function that takes the parameters xs and params, in that order,
                        where xs is a state vector of the system and params is a list of 
                        parameters, and returns the derivative of the system.
        params: A (numpy array) vector of parameters.
        state_inits: A (numpy array) vector of initial states.
        t_max: Time to simulate out to, in (arbitrary) seconds.
        n_times: The number of points to record. The higher this number, the higher
                    the time resolution of the simulation.
                    
    Returns: A SimulationData object, which is a named tuple containing params,
                ts (times, as a n_times-long vector), and solution (as a <# species>x<n_times>
                numpy array).      
    '''
    t0 = 0
    dt = (t_max - t0) / n_times
    ts = np.linspace(t0, t_max, n_times)

    def dv_dt(t, xs):
        return system_dv_dt(xs, params)
    
    ode = scipy.integrate.ode(dv_dt).set_integrator('lsoda')#, method='bdf', order = 5)
    ode.set_initial_value(state_inits, t0)
    solution = -1 * np.ones((n_times, len(state_inits)))
    solution[0,:] = state_inits
    i = 1
    while ode.successful() and ode.t < t_max and i < n_times:
        solution[i,:] = ode.integrate(ode.t+dt)
        i += 1

    return SimulationData(params = params, ts = ts, solution = solution)

from collections import namedtuple
SimulationData = namedtuple("SimulationData", ["params", "ts", "solution"])

def GH_well_mixed_dvdt(xs, params):
	Q, A, R = xs
	k_QA = params["k_QA"]
	k_AR = params["k_AR"]
	k_RQ = params["k_RQ"]

	dQ_dt = k_RQ * R - k_QA * A * Q
	dA_dt = k_QA * A * R - k_AR * A
	dR_dt = k_AR * A - k_RQ * R

	return np.array([dQ_dt, dA_dt, dR_dt])

def main():
	params = {
		"k_QA": 1,
		"k_AR": 0.6,
		"k_RQ": 0.03
		}

	init_Q = 1
	init_A = 0.1
	init_R = 0.1
	init_state = np.array([init_Q, init_A, init_R])

	names = ["Q", "A", "R"]
	simdata = simulate(GH_well_mixed_dvdt, 
	                   params, init_state, 
	                   t_max = 200, n_times = 10000)
	data = simdata.solution
	ts = simdata.ts

	plt.figure(figsize=(8,5))

	for i in range(len(names)):
		plt.plot(ts, data[:, i], color = dark_safe_colors[i], label = names[i], lw = 5)
	plt.xlabel("Time (sec)")
	plt.ylabel("Concentration (arbitrary)")
	#plt.title("Well-Mixed GH CRN")
	plt.legend(fontsize=26)
	plt.tight_layout()
	plt.savefig("GH_well_mixed.png", dpi=300)
	plt.show()

if __name__ == "__main__":
	main()