package HUOP;


/**
 * This class represents an Element of a utility-list as used by the QFWO algorithm.
 * 
 * @see AlgoQFWO_20160801
 * @see UO_List
 * @author Wensheng Gan, HIT, IIIRC
 */
class Element {
	// The three variables as described in the paper:
	/** transaction id */
	final int tid ;   
	
	/** itemset utility occupancy in each transaction (tid) */
	final double uo; 
	
	/** itemset remaining utility occupancy in each transaction (tid) */
	final double ruo; 
	
	/**
	 * Constructor.
	 * @param tid  the transaction id
	 * @param iutils  the itemset utility occupancy
	 * @param rutils  the itemset remaining utility occupancy
	 */
	public Element(int tid, double uo, double ruo){
		this.tid = tid;
		this.uo = uo;
		this.ruo = ruo;
	}

	public void showw(){
		System.out.println(this.tid + " " + this.uo + " " + this.ruo);
	}

}
