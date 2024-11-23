package HUOP;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * This class represents a UO-list as used by the HUOP algorithm.
 *
 * @see AlgoHUOP_20160801
 * @see Element
 * @author Wensheng Gan, HIT, IIIRC
 */
class UO_List {
	int item;  // the itemset
	double sumUO = 0;  // the sum of itemset utility occupancy
	double sumRUO = 0;  // the sum of itemset remaining utility occupancy

	int support = 0;
	List<Element> elements = new ArrayList<Element>();  // the elements
	
	/**
	 * Constructor.
	 * @param item the item that is used for this UO-list
	 */
	public UO_List(int item){
		this.item = item;
	}
	
	/**
	 * Method to add an element to this UO-list and update the sums at the same time.
	 * @param double1 
	 */
	public void addElement(Element element){
		sumUO += element.uo;
		sumRUO += element.ruo;
		elements.add(element);
		support++; // update the support
	}
	
	/**
	 * Get the sum UO
	 * @return
	 */
	public double getAvegUO(){
		return sumUO/support;
	}
	
	/**
	 * Get the sum RUO
	 * @return
	 */
	public double getAvegRUO(){
		return sumRUO/support;
	}

	public void showElement(){
		System.out.println(" _______ ");
		for (Element element : elements) {
			element.showw();
		}
	}
	
}
