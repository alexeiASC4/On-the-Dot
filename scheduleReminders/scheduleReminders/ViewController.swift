//
//  ViewController.swift
//  scheduleReminders
//
//  Created by Dylan Van Bramer on 5/1/22.
//

import UIKit

class ViewController: UIViewController {

        
    
    lazy var calendarView: UITableView = {
        let tableView = UITableView()
        tableView.register(EventCell.self, forCellReuseIdentifier: EventCell.id)
        tableView.dataSource = self
        tableView.delegate = self
        return tableView
    }()
    
    var mainTitle: UILabel = {
        let label = UILabel()
        label.font = .systemFont(ofSize: 45, weight: .black)
        label.textColor = .black
        label.text = "Name's Cornell Calendar"
        return label
    }()
    
    var pushButton: UIButton = {
        let button = UIButton()
        button.setTitle("Add New Event", for: .normal)
        button.addTarget(self, action: #selector(pushViewController), for: .touchUpInside)
        button.setTitleColor(.white, for: .normal)
        button.backgroundColor = .white
        button.layer.borderWidth = 3
        button.layer.cornerRadius = 15
        return button
    }()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        title = "Calendar View"
        
        [ mainTitle, calendarView ].forEach { subView in
            subView.translatesAutoresizingMaskIntoConstraints = false
            view.addSubview(subView)
        }
        NSLayoutConstraint.activate([
        mainTitle.widthAnchor.constraint(equalTo: view.safeAreaLayoutGuide.widthAnchor),
        mainTitle.centerXAnchor.constraint(equalTo: view.centerXAnchor),
        mainTitle.heightAnchor.constraint(equalToConstant: 60),
        mainTitle.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 15),
        ])
        
    }
    
    @objc func pushViewController() {
        let newEventPage = NewEvent()
        //newEventPage.delegate = self
        navigationController?.pushViewController(newEventPage, animated: true)
    }

}

extension ViewController: UITableViewDataSource {

    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return eventList.count
    }
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: EventCell.id, for: indexPath) as! EventCell
        let event1 = eventList[indexPath.row]
        cell.populateCell(event: event1)
        return cell
    }
    func tableView(_ tableView: UITableView, commit editingStyle: UITableViewCell.EditingStyle, forRowAt indexPath: IndexPath) {
        if editingStyle == UITableViewCell.EditingStyle.delete {
            eventList.remove(at: indexPath.row)
            tableView.deleteRows(at: [indexPath], with: UITableView.RowAnimation.automatic)
        }
    }
    func changeEventBody(event: String) {
        //eventList[indexPath.row].text = event
    }

}
extension ViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 80
}
//    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
//        let editorController = EditorController()
//        editorController.delegate = self
//        navigationController?.pushViewController(editorController, animated: true)
//
//    }
}
