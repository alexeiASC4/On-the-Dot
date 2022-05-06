//
//  ViewController.swift
//  OnTheDot
//
//  Created by Kyle Betts on 2022-05-05.
//

import UIKit

class MainController: UIViewController {
    
    var isLogin = true
    
    var emailLabel: UILabel = {
        let label = UILabel()
        label.text = "Email:"
        label.font = .systemFont(ofSize: 30, weight: .medium)
        return label
    }()
    
    var passwordLabel: UILabel = {
        let label = UILabel()
        label.text = "Password:"
        label.font = .systemFont(ofSize: 30, weight: .medium)
        return label
    }()
    
    var emailField: UITextField = {
        let field = UITextField()
        field.placeholder = "Email"
        field.backgroundColor = .white
        field.textAlignment = .center
        field.font = .systemFont(ofSize: 20, weight: .light)
        field.borderStyle = .roundedRect
        field.keyboardType = .emailAddress
        return field
    }()
    
    var passwordField: UITextField = {
        let field = UITextField()
        field.placeholder = "Password"
        field.backgroundColor = .white
        field.textAlignment = .center
        field.font = .systemFont(ofSize: 20, weight: .light)
        field.borderStyle = .roundedRect
        return field
    }()
    
    var switchStateButton: UIButton = {
        let button = UIButton()
        button.setTitle("Don't have an account? Sign Up.", for: .normal)
        button.addTarget(self, action: #selector(switchState), for: .touchUpInside)
        button.setTitleColor(.black, for: .normal)
        button.titleLabel?.font =  .systemFont(ofSize: 15)
        return button
    }()
    
    var enterAppButton: UIButton = {
        let button = UIButton()
        button.setTitle("Login", for: .normal)
        button.addTarget(self, action: #selector(enterApp), for: .touchUpInside)
        button.setTitleColor(.black, for: .normal)
        button.backgroundColor = .white
        button.titleLabel?.font =  .systemFont(ofSize: 30)
        button.layer.cornerRadius = 15
        return button
    }()

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBlue
        title = "On the Dot"
        
        [emailLabel, passwordLabel, emailField, passwordField, switchStateButton, enterAppButton].forEach { subView in
            subView.translatesAutoresizingMaskIntoConstraints = false
            view.addSubview(subView)
        }
        
        setupConstraints()
    }
    
    func setupConstraints() {
        let largeSpacing: CGFloat = 50
        let smallSpacing: CGFloat = 20
        
        // Constraints for emailLabel
        NSLayoutConstraint.activate([
            emailLabel.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: largeSpacing),
            emailLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
        
        // Constraints for emailField
        NSLayoutConstraint.activate([
            emailField.topAnchor.constraint(equalTo: emailLabel.bottomAnchor, constant: smallSpacing),
            emailField.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            emailField.widthAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.8)
        ])
        
        // Constraints for passwordLabel
        NSLayoutConstraint.activate([
            passwordLabel.topAnchor.constraint(equalTo: emailField.bottomAnchor, constant: largeSpacing),
            passwordLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
        
        // Constraints for passwordField
        NSLayoutConstraint.activate([
            passwordField.topAnchor.constraint(equalTo: passwordLabel.bottomAnchor, constant: smallSpacing),
            passwordField.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            passwordField.widthAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.8)
        ])
        
        // Constraints for enterAppButton
        NSLayoutConstraint.activate([
            enterAppButton.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor, constant: -largeSpacing),
            enterAppButton.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            enterAppButton.widthAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.8)
        ])
        
        // Constraints for switchStateButton
        NSLayoutConstraint.activate([
            switchStateButton.bottomAnchor.constraint(equalTo: enterAppButton.topAnchor, constant: -smallSpacing),
            switchStateButton.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            switchStateButton.widthAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.8)
        ])
        
    }
    
    @objc func switchState() {
        if isLogin {
            self.enterAppButton.setTitle("Sign Up", for: .normal)
            self.switchStateButton.setTitle("Already have an account? Login.", for: .normal)
            isLogin = false
        } else {
            self.enterAppButton.setTitle("Login", for: .normal)
            self.switchStateButton.setTitle("Don't have an account? Sign Up.", for: .normal)
            isLogin = true
        }
    }
    
    @objc func enterApp() {
    }

}

