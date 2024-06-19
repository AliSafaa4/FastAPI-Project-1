#include <iostream>
#include <vector>
using namespace std;

int nersetStaionIndex(int car_pos,vector<int> locations){
    int leftNersetLoc = 0;
    int rightNersetLoc = 0;

    for (int i=0; i < locations.size(); i++) {
        if (locations[i] == car_pos) {
            return locations[i];
        }
        if (locations[i] < car_pos) {
            leftNersetLoc = locations[i];
        } else if (locations[i] > car_pos) {
            rightNersetLoc = locations[i];
        }
    }

    
}

int main () {


    return 0;
}