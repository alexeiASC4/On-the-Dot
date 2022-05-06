//
//  NetworkManager.swift
//  OnTheDot
//
//  Created by Kyle Betts on 2022-05-05.
//

import Alamofire
import Foundation

struct NetworkManager {
    static let host = "http:localhost:8000"
    
    static func createUser(completion: @escaping (User) -> Void) {
        let endpoint = "\(host)/api/user/"
//        AF.request(endpoint, method: .post).validate().responseData { response in
//            switch (response.result) {
//            case .success(let data):
//                let jsonDecoder = JSONDecoder()
//                if let userResponse = try ? jsonDecoder.decode(User.self, from: data) {
//                    print(userResponse)
//                } else {
//                    print("Failed to decode getUsers")
//                }
//                    
//            case .failure(let error):
//                print(error.localizedDescription)
//            }
//        }
    }
}
