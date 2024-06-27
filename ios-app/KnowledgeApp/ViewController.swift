import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var titleLabel: UITextField!
    @IBOutlet weak var contentTextView: UITextView!

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    @IBAction func saveEntry(_ sender: UIButton) {
        guard let title = titleLabel.text, !title.isEmpty,
              let content = contentTextView.text, !content.isEmpty else {
            let alert = UIAlertController(title: "Error", message: "Please enter both title and content.", preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
            self.present(alert, animated: true, completion: nil)
            return
        }

        let url = URL(string: "http://127.0.0.1:5000/entry")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let entry = ["title": title, "content": content]
        let jsonData = try! JSONSerialization.data(withJSONObject: entry, options: [])

        let task = URLSession.shared.uploadTask(with: request, from: jsonData) { data, response, error in
            guard let data = data, error == nil else {
                print("Error: \(error?.localizedDescription ?? "No data")")
                return
            }

            let responseJSON = try? JSONSerialization.jsonObject(with: data, options: [])
            if let responseJSON = responseJSON as? [String: Any] {
                print("Response: \(responseJSON)")
            }
        }
        
        task.resume()

        titleLabel.text = ""
        contentTextView.text = ""
    }
}
