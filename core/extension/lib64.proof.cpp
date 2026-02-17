#include <openssl/sha.h>
#include <string>
#include <sstream>
#include <iomanip>
#include <cstring>

extern "C" {

void mine(const char* base_data, int difficulty, char output_hash[65], unsigned long long* final_nonce) {

    unsigned long long nonce = 0;
    std::string target(difficulty, '0');

    while (true) {
        std::string input = std::string(base_data) + std::to_string(nonce);

        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256((unsigned char*)input.c_str(), input.size(), hash);

        std::stringstream ss;
        for(int i = 0; i < SHA256_DIGEST_LENGTH; i++)
            ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];

        std::string hash_str = ss.str();

        if(hash_str.substr(0, difficulty) == target) {
            std::strncpy(output_hash, hash_str.c_str(), 65);
            *final_nonce = nonce;
            return;
        }

        nonce++;
    }
}



}