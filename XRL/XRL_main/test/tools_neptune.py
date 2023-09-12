import neptune.new as neptune

class neptune_log:
    def __init__(self, params):
        self.parameter = params

        run = neptune.init(
            project="xhnfirst/First-Test",
            api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI1NTg5MDI2OS01MTVmLTQ2YjUtODA1Yy02ZWQyNDgxZDcwN2UifQ==",
        )

            # Track metadata and hyperparameters of your Run
            run["Project Name"] = "NPT-952"
            run["algorithm"] = "ConvNet"
            run["parameters"] = self.parameter



if __name__ == "__main__":

    params = {
        "batch_size": 128,
        "dropout": 0.2,
        "learning_rate": 0.001,
        "optimizer": "Adam"
    }



# Track the training process by logging your training metrics
for epoch in range(100):
    run["train/accuracy"].log(epoch * 0.6)
    run["train/loss"].log(epoch * 0.4)

# Log the final results
run["f1_score"] = 0.66

# Stop logging to your Run
run.stop()
