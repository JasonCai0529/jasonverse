#include <opencv2/opencv.hpp>
using namespace cv;

int main(int argc, char** argv) {
    if (argc != 3) return 1;

    std::string input = argv[1];
    std::string output = argv[2];

    Mat image = imread(input);
    if (image.empty()) return 2;

    Mat gray;
    cvtColor(image, gray, COLOR_BGR2GRAY);
    imwrite(output, gray);

    return 0;
}
