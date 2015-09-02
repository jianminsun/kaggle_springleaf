#install.packages("readr")
#install.packages("xgboost")
library(readr)
library(xgboost)

set.seed(8675309)  # I got it I got it!

# Load train and test data
cat("reading the train and test data\n")
setwd("~/data-science/kaggle_springleaf")
train <- read_csv("./data/train_v3.csv", na = c(""))#,NA,-1,9999,999)) # from Bluefool
test  <- read_csv("./data/test_v3.csv")

# Remove variables with 0 variance - ones that have 1 unique value
# Code modified from raddar's Removing irrelevant VARS script
cat("Remove variables with 0 variance\n")
train.unique.count <- lapply(train, function(x) length(unique(x)))
train.unique.count_1 <- unlist(train.unique.count[unlist(train.unique.count) == 1])
delete_const <- names(train.unique.count_1)
print(length(c(delete_const)))

# Update train and test data
cat("Update train and test data\n")
train <- train[,!(names(train) %in% c(delete_const))]
test  <- test[,!(names(test) %in% c(delete_const))]
print(dim(train))
print(dim(test))
rm(train.unique.count, train.unique.count_1, delete_const)
gc()

cat("\n assuming text variables are categorical & replacing them with numeric ids\n")
#feature.names <- c(names(train)[2:1865], names(train)[1867:ncol(train)]) 
feature.names <-names(train)[2:ncol(train)]
#feature.names
for (f in feature.names) {
  if (class(train[[f]])=="character") {
    levels <- unique(c(train[[f]], test[[f]]))
    train[[f]] <- as.integer(factor(train[[f]], levels=levels))
    test[[f]]  <- as.integer(factor(test[[f]],  levels=levels))
  }
}

cat("\n replacing missing values with -1\n")
train[is.na(train)] <- -1
test[is.na(test)]   <- -1

cat("\n sampling train to get around 8GB memory limitations\n")
train <- train[sample(nrow(train), 55000),]
gc()

# Break into training and validation files method from Michael Pawlus
cat("\n Break training into training and validation\n")
nrow(train)
rws <- sample(nrow(train), 40000)
val <- train[-rws,]
gc()
train <- train[rws,]
gc()

# Prepare Data
cat("\n Prepare data for modeling\n")

cat(" Training data\n")
dtrain <- xgb.DMatrix(data.matrix(train[,feature.names]), label = train$target)
train <- train[1:2,]  # Becuase memory is constrained
gc()

cat(" Validation data\n")
dval   <- xgb.DMatrix(data.matrix(val[,feature.names]), label = val$target)
val <- val[1:2,]  # Tidy up the work space
gc()

watchlist <- watchlist <- list(eval = dval)
param <- list(objective = "binary:logistic",
              eta = .025,
              max_depth = 10,
              subsample = 0.7,
              colsample_bytree = 0.6,
              eval_metric = "auc"
              )

cat("training a XGBoost classifier\n")
clf <- xgb.train(params = param,
                 data = dtrain,
                 nrounds = 200,
                 verbose = 2,
                 early.stop.round = 5,
                 watchlist = watchlist,
                 maximize = TRUE,
                 print.every.n = 5
                 )

# Clean up
dtrain <- 0
gc()
dval <- 0
gc()

cat("making predictions in batches due to 8GB memory limitation\n")
submission <- data.frame(ID=test$ID)
submission$target <- NA
for (rows in split(1:nrow(test), ceiling((1:nrow(test))/10000))) {
    submission[rows, "target"] <- predict(clf, data.matrix(test[rows,feature.names]))
}

cat("saving the submission file\n")
write_csv(submission, "xgboost_submission.csv")
